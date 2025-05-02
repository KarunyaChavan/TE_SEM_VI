import sys
import sqlite3
import random
import math
from experta import KnowledgeEngine, Fact, Rule, MATCH, AS
import tkinter as tk
from tkinter import ttk, messagebox

BUFFER = 30  # Buffer time in minutes for runway availability

# -------------------- Database Setup --------------------
def initialize_database():
    conn = sqlite3.connect('pushpaka.db')
    cursor = conn.cursor()
    # Drop old tables if they exist (clear DB)
    cursor.execute("DROP TABLE IF EXISTS flights")
    cursor.execute("DROP TABLE IF EXISTS cargo")
    # Recreate flights table with additional columns:
    # fuel_capacity, plane_capacity, and free_time.
    cursor.execute('''
        CREATE TABLE flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            destination TEXT,
            time TEXT,
            distance INTEGER,
            plane TEXT,
            runway INTEGER,
            priority REAL,
            fuel_capacity INTEGER,
            plane_capacity INTEGER,
            free_time TEXT
        )
    ''')
    # Recreate cargo table with flight_id column to link cargo to a flight.
    cursor.execute('''
        CREATE TABLE cargo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo_name TEXT,
            destination TEXT,
            weight INTEGER,
            flight_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()


# -------------------- Helper Functions --------------------
def convert_HHMM_to_minutes(time_str):
    hour = int(time_str[:2])
    minute = int(time_str[2:])
    return hour * 60 + minute

def convert_minutes_to_HHMM(total_minutes):
    hour = (total_minutes // 60) % 24
    minute = total_minutes % 60
    return f"{hour:02d}{minute:02d}"

def calculate_free_time(departure_time, distance):
    """
    Calculates free time based on departure time (HHMM) and distance (km).
    Assumes an average speed of 10 km/min.
    """
    dep_minutes = convert_HHMM_to_minutes(departure_time)
    flight_duration = math.ceil(distance / 10)  # 10 km per minute
    free_minutes = dep_minutes + flight_duration
    return convert_minutes_to_HHMM(free_minutes)


# -------------------- Experta Engine --------------------
class Flight(Fact):
    """Fact for flight details"""
    pass

class Cargo(Fact):
    """Fact for cargo details"""
    pass

class PushpakaEngine(KnowledgeEngine):

    @Rule(Flight())
    def intelligent_fuel_check(self):
        print("🧠 Rule Fired: intelligent_fuel_check")

    @Rule(AS.f << Flight(source=MATCH.source, destination=MATCH.destination, time=MATCH.time, distance=MATCH.distance))
    def schedule_flight(self, f, source, destination, time, distance):
        conn = self.connect()
        cursor = conn.cursor()
        # Duplicate check:
        cursor.execute("""
            SELECT COUNT(*) FROM flights 
            WHERE source=? AND destination=? AND time=? AND distance=?
        """, (source, destination, time, distance))
        result = cursor.fetchone()
        print("DEBUG: Duplicate count =", result[0])
        if result[0] > 0:
            dup_message = (
                "\n⚠️ Duplicate Entry Detected:\n"
                f"    Flight from '{source}' to '{destination}' is already scheduled at {time} with a distance of {distance} km.\n"
                "    Note: If the destination is the same, then either or both of the time and distance should differ to indicate a different route.\n"
            )
            print(dup_message)
            messagebox.showwarning("Duplicate Flight", 
                                   f"Flight from '{source}' to '{destination}' at {time} ({distance} km) already exists.\n"
                                   "Please modify time and/or distance for a new route.")
            self.reset()  # Reset engine for next operation
            conn.close()
            return

        # Calculate fuel needed based on weather.
        weather = random.choice(["Clear", "Cloudy", "Stormy"])
        extra_fuel = 200 if weather != "Stormy" else 500
        fuel_needed = distance + extra_fuel
        print(f"🌤️ Weather: {weather}")
        print(f"⛽ Fuel Needed: {fuel_needed} km")

        planes = [("PN-101", 2200), ("PN-102", 2400), ("PN-103", 2600)]
        new_dep_minutes = convert_HHMM_to_minutes(time)
        selected_plane = None
        selected_fuel_capacity = None
        selected_runway = None

        for i, (plane, fuel_capacity) in enumerate(planes):
            if fuel_needed > fuel_capacity:
                continue
            cursor.execute("SELECT free_time FROM flights WHERE plane=? ORDER BY free_time DESC LIMIT 1", (plane,))
            row = cursor.fetchone()
            if row is None:
                selected_plane = plane
                selected_fuel_capacity = fuel_capacity
                selected_runway = i + 1
                break
            else:
                last_free_time = row[0]
                free_minutes = convert_HHMM_to_minutes(last_free_time)
                if new_dep_minutes >= free_minutes + BUFFER:
                    selected_plane = plane
                    selected_fuel_capacity = fuel_capacity
                    selected_runway = i + 1
                    break

        if selected_plane is None:
            print("❌ No available planes meet fuel or timing conditions.")
            messagebox.showwarning("Scheduling Failed", "No available planes meet fuel or timing conditions.")
            self.reset()
            conn.close()
            return

        runway = selected_runway
        priority = round((selected_fuel_capacity - fuel_needed) / selected_fuel_capacity * 100, 2)
        plane_capacity = int(2.5 * selected_fuel_capacity - 4500)
        free_time = calculate_free_time(time, distance)
        print(f"✅ Scheduled: {source} → {destination} at {time}")
        print(f"    Plane: {selected_plane} | Fuel: {selected_fuel_capacity} km | Runway: {runway}")
        print(f"    Priority: {priority}% | Cargo Cap: {plane_capacity} kg | Free Time: {free_time}")
        cursor.execute("""
            INSERT INTO flights (source, destination, time, distance, plane, runway, priority, fuel_capacity, plane_capacity, free_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source, destination, time, distance, selected_plane, runway, priority, selected_fuel_capacity, plane_capacity, free_time))
        conn.commit()
        messagebox.showinfo("Success", f"Flight scheduled successfully: {source} → {destination} at {time}.")
        self.reset()  # Reset engine for next operation
        conn.close()

    @Rule(Cargo(cargo_name=MATCH.cargo_name, destination=MATCH.destination, weight=MATCH.weight))
    def add_cargo(self, cargo_name, destination, weight):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, plane, plane_capacity FROM flights
            WHERE destination=?
        """, (destination,))
        flight = cursor.fetchone()
        if not flight:
            msg = f"❌ No flight scheduled for destination {destination}."
            print(msg)
            messagebox.showwarning("No Flight Found", f"No flight scheduled for destination {destination}.")
            self.reset()
            conn.close()
            return
        flight_id, plane, capacity = flight
        cursor.execute("SELECT SUM(weight) FROM cargo WHERE flight_id=?", (flight_id,))
        current_load = cursor.fetchone()[0]
        if current_load is None:
            current_load = 0
        if current_load + weight > capacity:
            msg = f"❌ Cannot add cargo '{cargo_name}': capacity exceeded for Plane {plane}."
            print(msg)
            messagebox.showwarning("Capacity Exceeded", f"Adding cargo '{cargo_name}' exceeds capacity for Plane {plane}.")
            self.reset()
            conn.close()
            return
        cursor.execute("INSERT INTO cargo (cargo_name, destination, weight, flight_id) VALUES (?, ?, ?, ?)",
                       (cargo_name, destination, weight, flight_id))
        conn.commit()
        success_msg = f"✅ Cargo '{cargo_name}' ({weight} kg) added for {destination} on Plane {plane}."
        print(success_msg)
        messagebox.showinfo("Success", f"Cargo '{cargo_name}' added successfully for {destination} on Plane {plane}.")
        self.reset()
        conn.close()

    def show_all_flights(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()
        conn.close()
        if flights:
            print("\n📋 Upcoming Flights:")
            for f in flights:
                print(f"ID:{f[0]} | {f[1]} → {f[2]} at {f[3]} | Dist: {f[4]} km | Plane: {f[5]} | Priority: {f[7]}%")
        else:
            print("🚫 No flights scheduled.")

    def show_flights_with_matching_cargo(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id, f.source, f.destination, f.time, f.distance, f.plane, f.runway, f.priority,
                   f.fuel_capacity, f.plane_capacity, f.free_time, c.cargo_name, c.weight
            FROM flights f JOIN cargo c ON f.id = c.flight_id
        """)
        results = cursor.fetchall()
        conn.close()
        if results:
            print("\n🔗 Flights with Matching Cargo:")
            for row in results:
                print(f"Flight {row[0]}: {row[1]} → {row[2]} at {row[3]} | Cargo: {row[11]} ({row[12]} kg)")
        else:
            print("🚫 No matching flights with cargo found.")

    def connect(self):
        return sqlite3.connect('pushpaka.db')


# -------------------- Output Redirector --------------------
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, s):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")
    def flush(self):
        pass


# -------------------- Tkinter GUI --------------------
class PushpakaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PUSHPAKA AIRLINES ✈️")
        self.root.geometry("950x700")
        self.root.configure(bg="#F7F9FC")
        
        # Style settings
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 12), padding=8)
        self.style.configure("TLabel", font=("Segoe UI", 12))
        self.style.configure("TEntry", font=("Segoe UI", 12))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#F7F9FC")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 14, "bold"), background="#F7F9FC")
        self.style.configure("TFrame", background="#F7F9FC")
        
        # Main container frames
        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)
        
        # A dedicated console area at the bottom.
        self.console_frame = ttk.Frame(self.root, style="TFrame")
        self.console_frame.pack(side="bottom", fill="both", padx=20, pady=(0,10))
        ttk.Label(self.console_frame, text="Console Output:", style="SubHeader.TLabel").pack(anchor="w")
        
        self.console_text = tk.Text(self.console_frame, height=10, state="disabled", font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4")
        self.console_text.pack(fill="both", expand=True)
        console_scroll = ttk.Scrollbar(self.console_frame, orient="vertical", command=self.console_text.yview)
        self.console_text.configure(yscroll=console_scroll.set)
        console_scroll.pack(side="right", fill="y")
        
        # Redirect standard output so nothing prints to terminal.
        sys.stdout = TextRedirector(self.console_text)
        
        # Store the clear console function reference for engine callbacks.
        self.clear_console_func = self.clear_console
        
        # Initialize the experta engine and reset it.
        self.engine = PushpakaEngine()
        self.engine.reset()
        self.engine.clear_console_func = self.clear_console
        
        # Create the improved menu.
        self.create_menu()
    
    def clear_console(self):
        self.console_text.configure(state="normal")
        self.console_text.delete("1.0", tk.END)
        self.console_text.configure(state="disabled")
    
    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_menu(self):
        self.clear_screen()
        header = ttk.Label(self.main_frame, text="✈️ PUSHPAKA AIRLINES SYSTEM", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=2, pady=20)
        
        btn_frame = ttk.Frame(self.main_frame, style="TFrame")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="✈️\nSchedule a Flight", command=self.schedule_flight_ui, width=20).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(btn_frame, text="📦\nAdd Cargo", command=self.add_cargo_ui, width=20).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(btn_frame, text="📋\nView All Flights", command=self.view_all_flights_ui, width=20).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(btn_frame, text="🔗\nFlights with Cargo", command=self.view_flights_with_cargo_ui, width=20).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(btn_frame, text="❌\nExit", command=self.root.quit, width=20).grid(row=2, column=0, columnspan=2, padx=10, pady=20)
    
    def schedule_flight_ui(self):
        self.clear_screen()
        ttk.Label(self.main_frame, text="🛫 Schedule a Flight", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        labels = [
            ("Source Airport (e.g., Pune)", "Source"),
            ("Destination City (e.g., Delhi)", "Destination"),
            ("Time (24hr, e.g., 0930)", "Time (HHMM)"),
            ("Distance (km, e.g., 1200)", "Distance (km)")
        ]
        self.flight_entries = {}
        for idx, (text, key) in enumerate(labels, start=1):
            ttk.Label(self.main_frame, text=text).grid(row=idx, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(self.main_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            self.flight_entries[key] = entry
        
        btn_frame = ttk.Frame(self.main_frame, style="TFrame")
        btn_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Submit", command=self.schedule_flight).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Back", command=self.create_menu).grid(row=0, column=1, padx=10)
    
    def schedule_flight(self):
        try:
            source = self.flight_entries["Source"].get().strip()
            dest = self.flight_entries["Destination"].get().strip()
            time_str = self.flight_entries["Time (HHMM)"].get().strip()
            distance = int(self.flight_entries["Distance (km)"].get().strip())
            if len(time_str) != 4 or not time_str.isdigit():
                raise ValueError("Time must be in HHMM format (e.g., 0930)")
            self.clear_console()
            self.engine.declare(Flight(source=source, destination=dest, time=time_str, distance=distance))
            self.engine.run()
            # On successful scheduling, a success message is shown via the rule.
            self.engine.reset()
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
    
    def add_cargo_ui(self):
        self.clear_screen()
        ttk.Label(self.main_frame, text="📦 Add Cargo", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        labels = [
            ("Cargo Name (e.g., Electronics)", "Cargo Name"),
            ("Destination City (e.g., Delhi)", "Destination"),
            ("Weight (kg, e.g., 500)", "Weight (kg)")
        ]
        self.cargo_entries = {}
        for idx, (text, key) in enumerate(labels, start=1):
            ttk.Label(self.main_frame, text=text).grid(row=idx, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(self.main_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            self.cargo_entries[key] = entry
        
        btn_frame = ttk.Frame(self.main_frame, style="TFrame")
        btn_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Submit", command=self.add_cargo).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Back", command=self.create_menu).grid(row=0, column=1, padx=10)
    
    def add_cargo(self):
        try:
            name = self.cargo_entries["Cargo Name"].get().strip()
            dest = self.cargo_entries["Destination"].get().strip()
            weight = int(self.cargo_entries["Weight (kg)"].get().strip())
            self.clear_console()
            self.engine.declare(Cargo(cargo_name=name, destination=dest, weight=weight))
            self.engine.run()
            # On successful cargo addition, the rule displays a success message.
            self.engine.reset()
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
    
    def view_all_flights_ui(self):
        self.clear_screen()
        ttk.Label(self.main_frame, text="📋 All Flights", style="Header.TLabel").pack(pady=10)
        table_frame = ttk.Frame(self.main_frame, style="TFrame")
        table_frame.pack(pady=5, fill="both", expand=True)
        cols = ("ID", "Source", "Destination", "Time", "Dist(km)", "Plane", "Runway", "Priority", "Fuel", "Capacity", "Free Time")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=80)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        conn = sqlite3.connect('pushpaka.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flights")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
        ttk.Button(self.main_frame, text="Back", command=self.create_menu).pack(pady=10)
    
    def view_flights_with_cargo_ui(self):
        self.clear_screen()
        ttk.Label(self.main_frame, text="🔗 Flights with Cargo", style="Header.TLabel").pack(pady=10)
        table_frame = ttk.Frame(self.main_frame, style="TFrame")
        table_frame.pack(pady=5, fill="both", expand=True)
        cols = ("ID", "Source", "Dest", "Time", "Dist", "Plane", "Runway", "Priority", "Fuel", "Cap", "Free", "Cargo", "Weight")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=70)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        conn = sqlite3.connect('pushpaka.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id, f.source, f.destination, f.time, f.distance, f.plane, f.runway, f.priority, 
                   f.fuel_capacity, f.plane_capacity, f.free_time, c.cargo_name, c.weight
            FROM flights f JOIN cargo c ON f.id = c.flight_id
        """)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
        ttk.Button(self.main_frame, text="Back", command=self.create_menu).pack(pady=10)


# -------------------- Main --------------------
if __name__ == "__main__":
    initialize_database()
    root = tk.Tk()
    app = PushpakaGUI(root)
    root.mainloop()
