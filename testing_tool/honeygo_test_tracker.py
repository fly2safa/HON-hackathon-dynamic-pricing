"""
HoneyGo Dynamic Pricing - Testing Tracker GUI Application
A standalone GUI tool for tracking manual testing progress.

Based on the TalentNest Testing Tracker pattern.
Adapted for HoneyGo Hackathon project.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import json
from datetime import datetime
from pathlib import Path
import webbrowser

# Try to import PIL for better image handling
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
RESULTS_DIR = SCRIPT_DIR / "results"

# Ensure results directory exists
RESULTS_DIR.mkdir(exist_ok=True)


class TestCase:
    """Represents a single test case."""
    
    def __init__(self, id, section, title, description, steps, hints=None):
        self.id = id
        self.section = section
        self.title = title
        self.description = description
        self.steps = steps
        self.hints = hints or []
        self.status = "Not Started"  # Not Started, Pass, Fail, Blocked
        self.actual_results = ""
        self.notes = ""
        self.tested_by = ""
        self.tested_date = ""


class HoneyGoTestingTracker:
    """Main GUI application for HoneyGo testing tracker."""
    
    VERSION = "1.0.0"  # Initial release with color-coded status
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"HoneyGo Testing Tracker v{self.VERSION}")
        self.root.geometry("1200x800")
        
        try:
            self.root.state("zoomed")
        except Exception:
            try:
                self.root.attributes("-zoomed", True)
            except Exception:
                pass
        
        self.root.minsize(1024, 768)
        
        # Configure colors
        self.colors = {
            'primary': '#FF6A13',      # Honeywell Orange
            'success': '#10b981',      # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Orange
            'info': '#06b6d4',         # Cyan
            'dark': '#1f2937',         # Dark gray
            'light': '#f3f4f6',        # Light gray
            'white': '#ffffff',
            'border': '#d1d5db'
        }
        
        # Setup styles
        self.setup_styles()
        
        # Test data
        self.test_cases = self.load_test_cases()
        self.current_test = None
        self.tester_name = ""
        self.has_unsaved_changes = False
        self.loaded_filename = None
        
        # Setup UI
        self.setup_ui()
        
        # Update progress
        self.update_progress()
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Prompt for tester name
        self.root.after(100, self.prompt_tester_name)
    
    def setup_styles(self):
        """Setup ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Treeview
        style.configure("Treeview",
                       background=self.colors['white'],
                       foreground=self.colors['dark'],
                       fieldbackground=self.colors['white'],
                       rowheight=30)
        style.configure("Treeview.Heading",
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10, 'bold'))
        style.map("Treeview",
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', self.colors['white'])])
        
        # Configure buttons
        style.configure("Primary.TButton",
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=(10, 5))
        style.configure("Success.TButton",
                       background=self.colors['success'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=(10, 5))
        style.configure("Danger.TButton",
                       background=self.colors['danger'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=(10, 5))
        
        # Configure colored radio buttons for status
        style.configure("Pass.TRadiobutton",
                       foreground="#059669",
                       font=('Segoe UI', 11, 'bold'))
        style.configure("Fail.TRadiobutton",
                       foreground="#dc2626",
                       font=('Segoe UI', 11, 'bold'))
        style.configure("Blocked.TRadiobutton",
                       foreground="#d97706",
                       font=('Segoe UI', 11, 'bold'))
        style.configure("NotStarted.TRadiobutton",
                       foreground="#6b7280",
                       font=('Segoe UI', 10))
    
    def load_test_cases(self):
        """Load predefined test cases for HoneyGo."""
        test_cases = []
        
        # ===== BACKEND HEALTH & CONNECTIVITY =====
        test_cases.extend([
            TestCase("1.1", "Backend", "Backend Server Start",
                    "Verify the FastAPI backend starts without errors",
                    ["Navigate to backend/ directory", 
                     "Activate virtual environment: source venv/Scripts/activate",
                     "Start server: uvicorn main:app --reload",
                     "Verify 'Uvicorn running on http://127.0.0.1:8000' appears"],
                    hints=["Check for any import errors in console",
                           "Verify .env file exists with required keys"]),
            TestCase("1.2", "Backend", "Health Check Endpoint",
                    "Verify /health endpoint returns healthy status",
                    ["Open browser to http://localhost:8000/health",
                     "Verify JSON response shows status: healthy",
                     "Check MongoDB connection status in response"],
                    hints=["You can also use: curl http://localhost:8000/health"]),
            TestCase("1.3", "Backend", "API Documentation",
                    "Verify Swagger UI is accessible",
                    ["Open http://localhost:8000/docs",
                     "Verify Swagger UI loads with all endpoints listed",
                     "Check /pricing/calculate endpoint is documented"],
                    hints=["ReDoc also available at /redoc"]),
            TestCase("1.4", "Backend", "MongoDB Connection",
                    "Verify backend connects to MongoDB Atlas",
                    ["Check backend startup logs for MongoDB connection",
                     "Verify '✅ MongoDB connected successfully' message",
                     "Test a simple query via API"],
                    hints=["Check MONGODB_URI in .env if connection fails"]),
        ])
        
        # ===== FRONTEND STARTUP =====
        test_cases.extend([
            TestCase("2.1", "Frontend", "Frontend Server Start",
                    "Verify Next.js frontend starts without errors",
                    ["Navigate to frontend/ directory",
                     "Run: npm run dev",
                     "Verify 'Ready on http://localhost:3000' appears"],
                    hints=["Run 'npm install' first if node_modules missing"]),
            TestCase("2.2", "Frontend", "Homepage Load",
                    "Verify homepage loads correctly with all components",
                    ["Open http://localhost:3000 in browser",
                     "Verify HoneyGo header/logo appears",
                     "Verify 'Live Market Conditions' section visible",
                     "Verify ride request cards are displayed"],
                    hints=["Check browser console for any errors (F12)"]),
            TestCase("2.3", "Frontend", "Backend Connection Banner",
                    "Verify backend connection status banner works",
                    ["With backend running, verify green 'Connected' indicator",
                     "Stop backend, refresh page",
                     "Verify red 'Disconnected' warning appears",
                     "Restart backend, verify reconnection"],
                    hints=["Banner should update automatically"]),
        ])
        
        # ===== LANGSMITH INTEGRATION =====
        test_cases.extend([
            TestCase("3.1", "LangSmith", "LangSmith Configuration",
                    "Verify LangSmith API key is properly configured",
                    ["Check .env file has LANGSMITH_API_KEY or LANGCHAIN_API_KEY",
                     "Verify LANGCHAIN_TRACING_V2=true",
                     "Verify LANGCHAIN_PROJECT=honeygo-pricing",
                     "Restart backend and check for '✅ LangSmith tracing enabled' log"],
                    hints=["Get API key from https://smith.langchain.com/settings"]),
            TestCase("3.2", "LangSmith", "Trace Generation",
                    "Verify pricing calculations generate LangSmith traces",
                    ["Ensure backend is running with LangSmith enabled",
                     "Click 'Calculate' on a ride in the frontend",
                     "Open LangSmith dashboard: https://smith.langchain.com/",
                     "Navigate to 'honeygo-pricing' project",
                     "Verify new trace appears within seconds"],
                    hints=["Traces show full prompt, response, latency, tokens"]),
            TestCase("3.3", "LangSmith", "Trace Details",
                    "Verify trace contains expected information",
                    ["Click on a trace in LangSmith dashboard",
                     "Verify system prompt is visible",
                     "Verify user prompt contains ride details",
                     "Verify model response is captured",
                     "Check latency and token usage"],
                    hints=["Look for route, distance, weather in the prompt"]),
        ])
        
        # ===== WEATHER INTEGRATION =====
        test_cases.extend([
            TestCase("4.1", "Weather", "Real Weather Display",
                    "Verify real weather data is fetched and displayed",
                    ["Select different cities in the dropdown",
                     "Observe Weather card in 'Live Market Conditions'",
                     "Verify '🌐 Live' badge appears for real weather",
                     "Check temperature and condition are realistic"],
                    hints=["Weather API key required in .env (WEATHER_API_KEY)"]),
            TestCase("4.2", "Weather", "Weather in AI Reasoning",
                    "Verify AI reasoning mentions actual weather conditions",
                    ["Select a city with non-clear weather (e.g., check NY)",
                     "Note the weather shown in the Weather card",
                     "Click 'Calculate' on a ride",
                     "Verify AI reasoning mentions matching weather condition"],
                    hints=["Weather types: clear, clouds, rain, snow, storm, fog"]),
            TestCase("4.3", "Weather", "Weather Fallback",
                    "Verify mock weather works when API is unavailable",
                    ["Remove or invalidate WEATHER_API_KEY in .env",
                     "Restart frontend",
                     "Select a city",
                     "Verify weather still displays (without Live badge)"],
                    hints=["Mock weather is generated based on city/season"]),
        ])
        
        # ===== DEMAND & SURGE PRICING =====
        test_cases.extend([
            TestCase("5.1", "Demand", "Demand Thermometer Display",
                    "Verify demand thermometer shows correct level",
                    ["Observe the Demand thermometer in Live Market Conditions",
                     "Note the level: Low, Medium, High, or Surge",
                     "Verify thermometer fill matches the label",
                     "Change cities and observe demand changes"],
                    hints=["Thermometer should animate smoothly"]),
            TestCase("5.2", "Demand", "Demand in AI Reasoning",
                    "Verify AI reasoning matches displayed demand level",
                    ["Note the current demand level from thermometer",
                     "Click 'Calculate' on a ride",
                     "Check first bullet in AI Reasoning",
                     "Verify it says '[City] - [Demand] demand detected'"],
                    hints=["This works in both mock and real backend modes"]),
            TestCase("5.3", "Demand", "Surge Multiplier",
                    "Verify surge pricing is applied during high demand",
                    ["Wait for or find a 'Surge' demand condition",
                     "Calculate a ride price",
                     "Verify surge multiplier > 1.0 is shown",
                     "Verify price explanation mentions surge"],
                    hints=["Surge can be triggered by time of day or events"]),
        ])
        
        # ===== LOYALTY TIER PRICING =====
        test_cases.extend([
            TestCase("6.1", "Loyalty", "Tier Selection",
                    "Verify loyalty tier dropdown works",
                    ["Locate the loyalty tier dropdown (New, Silver, Gold, Platinum)",
                     "Select 'Silver' tier",
                     "Verify the selection is highlighted",
                     "Try each tier to verify all options work"],
                    hints=["Tiers: New (0%), Silver (10%), Gold (15%), Platinum (20%)"]),
            TestCase("6.2", "Loyalty", "Discount Application",
                    "Verify loyalty discount is applied to price",
                    ["Select 'Silver' tier (10% discount)",
                     "Calculate a ride price",
                     "Compare 'Standard Price' vs 'AI Dynamic Price'",
                     "Verify ~10% discount is applied to final price"],
                    hints=["Check the exact discount in AI Reasoning"]),
            TestCase("6.3", "Loyalty", "Loyalty in AI Reasoning",
                    "Verify AI reasoning shows loyalty discount details",
                    ["Select 'Gold' tier",
                     "Calculate a ride price",
                     "Check AI Reasoning bullets",
                     "Verify last bullet shows 'GOLD member: 15% loyalty discount applied'"],
                    hints=["Shows exact dollar amount saved"]),
            TestCase("6.4", "Loyalty", "Competitor Price Consistency",
                    "Verify competitor prices don't change with loyalty tier",
                    ["Calculate a ride with 'New' tier, note Uber/Lyft prices",
                     "Change to 'Platinum' tier",
                     "Calculate same ride again",
                     "Verify competitor prices are same (discount only affects our price)"],
                    hints=["Competitor prices based on pre-discount price"]),
        ])
        
        # ===== CITY-SPECIFIC PRICING =====
        test_cases.extend([
            TestCase("7.1", "Cities", "City Selection",
                    "Verify city dropdown changes all relevant data",
                    ["Select 'Phoenix' from city dropdown",
                     "Verify ride cards show Phoenix locations",
                     "Verify weather updates for Phoenix",
                     "Select 'New York', verify everything updates"],
                    hints=["Cities: Phoenix, New York, San Francisco, Chicago, Orlando"]),
            TestCase("7.2", "Cities", "City Pricing Multipliers",
                    "Verify different cities have different base prices",
                    ["Add a ride in Phoenix, calculate price",
                     "Switch to New York, add similar distance ride",
                     "Calculate price",
                     "Verify NYC price is higher (cost of living factor)"],
                    hints=["NYC ~1.4x, SF ~1.35x, Chicago ~1.2x, Phoenix ~1.0x"]),
            TestCase("7.3", "Cities", "Waymo Availability",
                    "Verify Waymo only appears in supported cities",
                    ["Select Phoenix, calculate a ride",
                     "Verify Waymo price appears in competitor comparison",
                     "Switch to Chicago, calculate a ride",
                     "Verify Waymo is NOT shown (only Phoenix & SF)"],
                    hints=["Waymo operates in Phoenix and San Francisco"]),
            TestCase("7.4", "Cities", "City Comparison Modal",
                    "Verify city comparison feature works",
                    ["Click 'Compare Cities' or similar button",
                     "Verify modal shows pricing across all 5 cities",
                     "Verify 'Best Value' badge appears on cheapest",
                     "Close modal and verify main page is intact"],
                    hints=["Modal should show same ride across all cities"]),
        ])
        
        # ===== UI & ANIMATIONS =====
        test_cases.extend([
            TestCase("8.1", "UI", "Animated Components",
                    "Verify Steve's animations are working",
                    ["Observe Demand Thermometer - verify fill animation",
                     "Observe Available Drivers card - verify car animations",
                     "Observe Active Rides card - verify car animations",
                     "Observe Weather card - verify weather-specific animations"],
                    hints=["Cars should move, thermometer should pulse"]),
            TestCase("8.2", "UI", "No Duplicate Cards",
                    "Verify no duplicate market condition cards",
                    ["Check 'Live Market Conditions' section",
                     "Verify only ONE Demand card (thermometer version)",
                     "Verify only ONE Available Drivers card (animated)",
                     "Total should be 4 cards: Demand, Drivers, Active Rides, Weather"],
                    hints=["Bug fix removed old text-only cards"]),
            TestCase("8.3", "UI", "AI Reasoning Formatting",
                    "Verify AI reasoning displays as bullet points",
                    ["Calculate a ride price",
                     "Check 'AI Reasoning' section",
                     "Verify each reason is on its own line with number",
                     "Verify no run-on paragraphs"],
                    hints=["Should show numbered bullets (1, 2, 3, etc.)"]),
            TestCase("8.4", "UI", "Processing Animation",
                    "Verify AI thinking animation during calculation",
                    ["Click 'Calculate' on a ride",
                     "Observe the loading/thinking animation",
                     "Verify animation shows AI is processing",
                     "Verify smooth transition to results"],
                    hints=["Animation should be visible for 2-5 seconds"]),
        ])
        
        # ===== MOCK VS REAL BACKEND =====
        test_cases.extend([
            TestCase("9.1", "Mock/Real", "Backend Mode Detection",
                    "Verify app correctly detects backend availability",
                    ["With backend running, calculate a ride",
                     "Check browser console for '✅ Backend response'",
                     "Stop backend (Ctrl+C)",
                     "Calculate again, check for '❌ Backend pricing failed, falling back to mock'"],
                    hints=["Console messages indicate which mode is active"]),
            TestCase("9.2", "Mock/Real", "Mock Data Fallback",
                    "Verify mock data works when backend is down",
                    ["Stop the backend server",
                     "Refresh frontend",
                     "Calculate a ride price",
                     "Verify pricing still works (using mock data)",
                     "Verify AI reasoning is generated"],
                    hints=["Mock mode still provides full functionality"]),
            TestCase("9.3", "Mock/Real", "Seamless Transition",
                    "Verify smooth transition between mock and real",
                    ["Start with backend stopped, calculate a ride",
                     "Start the backend",
                     "Calculate another ride",
                     "Verify new calculation uses real backend",
                     "Check for LangSmith trace (real backend only)"],
                    hints=["No page refresh needed to switch modes"]),
        ])
        
        # ===== SCHEDULED RIDES =====
        test_cases.extend([
            TestCase("10.1", "Scheduling", "Add Scheduled Ride",
                    "Verify scheduled ride creation works",
                    ["Click 'Add Scheduled Ride' button",
                     "Select a future date and time",
                     "Verify ride card shows 'Scheduled' badge",
                     "Verify scheduled time is displayed on card"],
                    hints=["Date picker should appear for selection"]),
            TestCase("10.2", "Scheduling", "Scheduled Ride Pricing",
                    "Verify scheduled rides show estimated pricing",
                    ["Create a scheduled ride for future date",
                     "Calculate its price",
                     "Verify warning about 'Estimated Price' appears",
                     "Verify explanation mentions future conditions"],
                    hints=["Prices may vary at actual pickup time"]),
        ])
        
        # ===== END-TO-END SCENARIOS =====
        test_cases.extend([
            TestCase("11.1", "E2E", "Happy Path - Immediate Ride",
                    "Complete end-to-end test for immediate ride",
                    ["Select city: Phoenix",
                     "Select loyalty tier: Gold",
                     "Add a new ride (pickup now)",
                     "Click Calculate",
                     "Verify all components update correctly",
                     "Verify pricing shows Gold discount",
                     "Verify weather matches Phoenix conditions"],
                    hints=["This tests the main user flow"]),
            TestCase("11.2", "E2E", "Happy Path - Different Cities",
                    "Test pricing across multiple cities",
                    ["Test ride in Phoenix - note price",
                     "Test same distance ride in NYC - note price",
                     "Test same distance ride in SF - note price",
                     "Verify NYC > SF > Phoenix pricing",
                     "Verify LangSmith traces for all (if backend on)"],
                    hints=["Higher cost of living = higher prices"]),
            TestCase("11.3", "E2E", "Stress Test - Multiple Calculations",
                    "Verify app handles rapid calculations",
                    ["Rapidly click Calculate on different rides",
                     "Verify each calculation completes",
                     "Verify no UI freezing or errors",
                     "Check browser console for any errors"],
                    hints=["App should handle concurrent requests gracefully"]),
        ])
        
        return test_cases
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Header
        self.create_header(main_container)
        
        # Quick Jump buttons
        self.create_quick_jump(main_container)
        
        # Main content (paned window)
        paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned.grid(row=2, column=0, sticky="nsew", pady=10)
        
        # Left panel - Test list
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        self.create_test_list(left_frame)
        
        # Right panel - Test details
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        self.create_test_details(right_frame)
        
        # Footer
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create header section."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(2, weight=1)
        
        # Logo
        self.logo_image = None
        logo_path = SCRIPT_DIR.parent / "images" / "honeygo-logo.png"
        if logo_path.exists():
            try:
                if PIL_AVAILABLE:
                    # Use PIL for better image handling and resizing
                    img = Image.open(logo_path)
                    img = img.resize((40, 40), Image.Resampling.LANCZOS)
                    self.logo_image = ImageTk.PhotoImage(img)
                else:
                    # Fallback to tkinter PhotoImage (may not work with all PNGs)
                    self.logo_image = tk.PhotoImage(file=str(logo_path)).subsample(4, 4)
                
                logo_label = ttk.Label(header_frame, image=self.logo_image)
                logo_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
            except Exception as e:
                print(f"Could not load logo: {e}")
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="HoneyGo Testing Tracker",
                               font=('Segoe UI', 18, 'bold'),
                               foreground=self.colors['primary'])
        title_label.grid(row=0, column=1, sticky="w")
        
        # Progress
        self.progress_var = tk.StringVar(value="Progress: 0/0 (0%)")
        progress_label = ttk.Label(header_frame, textvariable=self.progress_var,
                                  font=('Segoe UI', 12))
        progress_label.grid(row=0, column=2, padx=20)
        
        # Tester name
        self.tester_var = tk.StringVar(value="Tester: Not set")
        tester_label = ttk.Label(header_frame, textvariable=self.tester_var,
                                font=('Segoe UI', 10))
        tester_label.grid(row=0, column=3, sticky="e")
        
        # Buttons frame
        btn_frame = ttk.Frame(header_frame)
        btn_frame.grid(row=0, column=4, padx=(20, 0))
        
        ttk.Button(btn_frame, text="💾 Save", command=self.save_results).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📂 Load", command=self.load_results).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📊 Report", command=self.generate_report).pack(side=tk.LEFT, padx=2)
    
    def create_quick_jump(self, parent):
        """Create quick jump buttons for sections."""
        jump_frame = ttk.LabelFrame(parent, text="Quick Jump to Section", padding="5")
        jump_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        sections = list(dict.fromkeys([tc.section for tc in self.test_cases]))
        
        for i, section in enumerate(sections):
            btn = ttk.Button(jump_frame, text=section, 
                           command=lambda s=section: self.jump_to_section(s))
            btn.grid(row=i//6, column=i%6, padx=2, pady=2, sticky="ew")
    
    def create_test_list(self, parent):
        """Create test list treeview."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Status",), show="tree headings")
        self.tree.heading("#0", text="Test Case")
        self.tree.heading("Status", text="Status")
        self.tree.column("#0", width=250)
        self.tree.column("Status", width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure color tags for status
        self.tree.tag_configure("pass", foreground="#059669", background="#ecfdf5")      # Green
        self.tree.tag_configure("fail", foreground="#dc2626", background="#fef2f2")      # Red
        self.tree.tag_configure("blocked", foreground="#d97706", background="#fffbeb")   # Orange
        self.tree.tag_configure("not_started", foreground="#6b7280")                      # Gray
        
        # Populate tree
        self.populate_tree()
        
        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self.on_test_select)
    
    def populate_tree(self):
        """Populate the test tree."""
        self.tree.delete(*self.tree.get_children())
        
        sections = {}
        for tc in self.test_cases:
            if tc.section not in sections:
                sections[tc.section] = self.tree.insert("", "end", text=tc.section, open=True)
            
            status_icon = self.get_status_icon(tc.status)
            tag = self.get_status_tag(tc.status)
            self.tree.insert(sections[tc.section], "end", 
                           iid=tc.id,
                           text=f"{tc.id}: {tc.title}",
                           values=(f"{status_icon} {tc.status}",),
                           tags=(tag,))
    
    def get_status_icon(self, status):
        """Get icon for status."""
        icons = {
            "Not Started": "⬜",
            "Pass": "✅",
            "Fail": "❌",
            "Blocked": "🚫"
        }
        return icons.get(status, "⬜")
    
    def get_status_tag(self, status):
        """Get color tag for status."""
        tags = {
            "Not Started": "not_started",
            "Pass": "pass",
            "Fail": "fail",
            "Blocked": "blocked"
        }
        return tags.get(status, "not_started")
    
    def create_test_details(self, parent):
        """Create test details panel."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(4, weight=1)
        
        # Test info
        info_frame = ttk.LabelFrame(parent, text="Test Case Details", padding="10")
        info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Title:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.title_var, wraplength=500).grid(row=0, column=1, sticky="w")
        
        ttk.Label(info_frame, text="Description:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky="nw", pady=(10,0))
        self.desc_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.desc_var, wraplength=500).grid(row=1, column=1, sticky="w", pady=(10,0))
        
        # Steps
        steps_frame = ttk.LabelFrame(parent, text="Test Steps", padding="10")
        steps_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        steps_frame.columnconfigure(0, weight=1)
        
        self.steps_text = scrolledtext.ScrolledText(steps_frame, height=5, wrap=tk.WORD,
                                                    font=('Consolas', 10))
        self.steps_text.grid(row=0, column=0, sticky="ew")
        self.steps_text.configure(state='disabled')
        
        # Hints
        hints_frame = ttk.LabelFrame(parent, text="💡 Hints", padding="10")
        hints_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        hints_frame.columnconfigure(0, weight=1)
        
        self.hints_text = scrolledtext.ScrolledText(hints_frame, height=3, wrap=tk.WORD,
                                                   font=('Segoe UI', 9), bg='#fffbeb')
        self.hints_text.grid(row=0, column=0, sticky="ew")
        self.hints_text.configure(state='disabled')
        
        # Status buttons with color coding
        status_frame = ttk.LabelFrame(parent, text="Set Status", padding="10")
        status_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Not Started")
        statuses = [
            ("⬜ Not Started", "Not Started", "NotStarted.TRadiobutton"),
            ("✅ Pass", "Pass", "Pass.TRadiobutton"), 
            ("❌ Fail", "Fail", "Fail.TRadiobutton"),
            ("🚫 Blocked", "Blocked", "Blocked.TRadiobutton")
        ]
        
        for i, (text, value, style_name) in enumerate(statuses):
            rb = ttk.Radiobutton(status_frame, text=text, value=value,
                               variable=self.status_var, command=self.on_status_change,
                               style=style_name)
            rb.grid(row=0, column=i, padx=15)
        
        # Notes
        notes_frame = ttk.LabelFrame(parent, text="Notes / Actual Results", padding="10")
        notes_frame.grid(row=4, column=0, sticky="nsew")
        notes_frame.columnconfigure(0, weight=1)
        notes_frame.rowconfigure(0, weight=1)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=8, wrap=tk.WORD,
                                                   font=('Segoe UI', 10))
        self.notes_text.grid(row=0, column=0, sticky="nsew")
        self.notes_text.bind("<<Modified>>", self.on_notes_change)
    
    def create_footer(self, parent):
        """Create footer with navigation."""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        ttk.Button(footer_frame, text="⬅ Previous", command=self.prev_test).pack(side=tk.LEFT)
        ttk.Button(footer_frame, text="Next ➡", command=self.next_test).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(footer_frame, text="🌐 Open LangSmith", 
                  command=lambda: webbrowser.open("https://smith.langchain.com/")).pack(side=tk.RIGHT)
        ttk.Button(footer_frame, text="📖 Open Docs", 
                  command=lambda: webbrowser.open("http://localhost:8000/docs")).pack(side=tk.RIGHT, padx=10)
        ttk.Button(footer_frame, text="🏠 Open Frontend", 
                  command=lambda: webbrowser.open("http://localhost:3000")).pack(side=tk.RIGHT, padx=10)
    
    def prompt_tester_name(self):
        """Prompt for tester name."""
        name = simpledialog.askstring("Tester Name", 
                                      "Enter your name:",
                                      parent=self.root)
        if name:
            self.tester_name = name.strip()
            self.tester_var.set(f"Tester: {self.tester_name}")
        else:
            self.tester_name = "Anonymous"
            self.tester_var.set("Tester: Anonymous")
    
    def on_test_select(self, event):
        """Handle test selection."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        
        # Find test case
        for tc in self.test_cases:
            if tc.id == item_id:
                self.current_test = tc
                self.display_test(tc)
                break
    
    def display_test(self, tc):
        """Display test case details."""
        self.title_var.set(f"{tc.id}: {tc.title}")
        self.desc_var.set(tc.description)
        
        # Steps
        self.steps_text.configure(state='normal')
        self.steps_text.delete(1.0, tk.END)
        for i, step in enumerate(tc.steps, 1):
            self.steps_text.insert(tk.END, f"{i}. {step}\n")
        self.steps_text.configure(state='disabled')
        
        # Hints
        self.hints_text.configure(state='normal')
        self.hints_text.delete(1.0, tk.END)
        for hint in tc.hints:
            self.hints_text.insert(tk.END, f"💡 {hint}\n")
        if not tc.hints:
            self.hints_text.insert(tk.END, "(No hints available)")
        self.hints_text.configure(state='disabled')
        
        # Status
        self.status_var.set(tc.status)
        
        # Notes
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(tk.END, tc.notes)
        self.notes_text.edit_modified(False)
    
    def on_status_change(self):
        """Handle status change."""
        if self.current_test:
            self.current_test.status = self.status_var.get()
            self.current_test.tested_by = self.tester_name
            self.current_test.tested_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.has_unsaved_changes = True
            self.update_tree_item(self.current_test)
            self.update_progress()
    
    def on_notes_change(self, event):
        """Handle notes change."""
        if self.current_test and self.notes_text.edit_modified():
            self.current_test.notes = self.notes_text.get(1.0, tk.END).strip()
            self.has_unsaved_changes = True
            self.notes_text.edit_modified(False)
    
    def update_tree_item(self, tc):
        """Update tree item for test case with color coding."""
        status_icon = self.get_status_icon(tc.status)
        tag = self.get_status_tag(tc.status)
        self.tree.item(tc.id, values=(f"{status_icon} {tc.status}",), tags=(tag,))
    
    def update_progress(self):
        """Update progress display."""
        total = len(self.test_cases)
        completed = sum(1 for tc in self.test_cases if tc.status in ["Pass", "Fail"])
        passed = sum(1 for tc in self.test_cases if tc.status == "Pass")
        failed = sum(1 for tc in self.test_cases if tc.status == "Fail")
        blocked = sum(1 for tc in self.test_cases if tc.status == "Blocked")
        pct = (completed / total * 100) if total > 0 else 0
        self.progress_var.set(f"Progress: {completed}/{total} ({pct:.0f}%) | ✅ {passed} | ❌ {failed} | 🚫 {blocked}")
    
    def jump_to_section(self, section):
        """Jump to first test in section."""
        for tc in self.test_cases:
            if tc.section == section:
                self.tree.selection_set(tc.id)
                self.tree.see(tc.id)
                self.tree.focus(tc.id)
                break
    
    def prev_test(self):
        """Go to previous test."""
        if self.current_test:
            idx = self.test_cases.index(self.current_test)
            if idx > 0:
                prev_tc = self.test_cases[idx - 1]
                self.tree.selection_set(prev_tc.id)
                self.tree.see(prev_tc.id)
    
    def next_test(self):
        """Go to next test."""
        if self.current_test:
            idx = self.test_cases.index(self.current_test)
            if idx < len(self.test_cases) - 1:
                next_tc = self.test_cases[idx + 1]
                self.tree.selection_set(next_tc.id)
                self.tree.see(next_tc.id)
    
    def save_results(self):
        """Save test results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = RESULTS_DIR / f"test_progress_{self.tester_name}_{timestamp}.json"
        
        data = {
            "tester": self.tester_name,
            "saved_at": datetime.now().isoformat(),
            "version": self.VERSION,
            "test_cases": []
        }
        
        for tc in self.test_cases:
            data["test_cases"].append({
                "id": tc.id,
                "status": tc.status,
                "notes": tc.notes,
                "tested_by": tc.tested_by,
                "tested_date": tc.tested_date
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.has_unsaved_changes = False
        self.loaded_filename = filename
        messagebox.showinfo("Saved", f"Results saved to:\n{filename}")
    
    def load_results(self):
        """Load test results from JSON."""
        filename = filedialog.askopenfilename(
            initialdir=RESULTS_DIR,
            title="Load Test Results",
            filetypes=[("JSON files", "*.json")]
        )
        
        if not filename:
            return
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Update test cases
        for tc_data in data.get("test_cases", []):
            for tc in self.test_cases:
                if tc.id == tc_data["id"]:
                    tc.status = tc_data.get("status", "Not Started")
                    tc.notes = tc_data.get("notes", "")
                    tc.tested_by = tc_data.get("tested_by", "")
                    tc.tested_date = tc_data.get("tested_date", "")
                    self.update_tree_item(tc)
                    break
        
        self.tester_name = data.get("tester", "Unknown")
        self.tester_var.set(f"Tester: {self.tester_name}")
        self.loaded_filename = filename
        self.has_unsaved_changes = False
        self.update_progress()
        messagebox.showinfo("Loaded", f"Results loaded from:\n{filename}")
    
    def generate_report(self):
        """Generate markdown report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = RESULTS_DIR / f"test_report_{self.tester_name}_{timestamp}.md"
        
        total = len(self.test_cases)
        passed = sum(1 for tc in self.test_cases if tc.status == "Pass")
        failed = sum(1 for tc in self.test_cases if tc.status == "Fail")
        blocked = sum(1 for tc in self.test_cases if tc.status == "Blocked")
        not_started = sum(1 for tc in self.test_cases if tc.status == "Not Started")
        
        report = f"""# HoneyGo Testing Report

**Tester:** {self.tester_name}
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Tool Version:** {self.VERSION}

## Summary

| Status | Count |
|--------|-------|
| ✅ Pass | {passed} |
| ❌ Fail | {failed} |
| 🚫 Blocked | {blocked} |
| ⬜ Not Started | {not_started} |
| **Total** | **{total}** |

**Pass Rate:** {(passed/total*100) if total > 0 else 0:.1f}%

## Test Results by Section

"""
        
        current_section = ""
        for tc in self.test_cases:
            if tc.section != current_section:
                current_section = tc.section
                report += f"\n### {current_section}\n\n"
            
            icon = self.get_status_icon(tc.status)
            report += f"- {icon} **{tc.id}: {tc.title}** - {tc.status}\n"
            if tc.notes:
                report += f"  - Notes: {tc.notes}\n"
        
        report += f"""
---
*Generated by HoneyGo Testing Tracker v{self.VERSION}*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        messagebox.showinfo("Report Generated", f"Report saved to:\n{filename}")
        webbrowser.open(filename)
    
    def on_closing(self):
        """Handle window close."""
        if self.has_unsaved_changes:
            if messagebox.askyesno("Unsaved Changes", 
                                   "You have unsaved changes. Save before closing?"):
                self.save_results()
        self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = HoneyGoTestingTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()

