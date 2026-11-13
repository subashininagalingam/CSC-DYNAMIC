"""
CSC Prospectus 2026 -- course catalogue.

Single source of truth for the programme pages (/courses/programs/).
All text below is taken from PROSPECTUS_2026.pdf. Only obvious spelling slips
were corrected (Phyton -> Python, reconcilliation -> reconciliation, ...).

Editing guide
-------------
* Shared syllabus blocks (MySQL, Python, Tally ...) are defined ONCE in
  ``BLOCKS`` and referenced by key, so a change shows up in every programme.
* A block holds either ``topics`` (a flat list) or ``groups`` (a list of
  ``(label, topics)``) for long syllabi such as Python.
"""
import re

_SPLIT = re.compile(r"\s+[-\u2013]\s+")


def T(text):
    """Split a prospectus line ('A - B - C.') into a clean topic list."""
    text = " ".join(text.split()).rstrip(".")
    return [t.strip(" .") for t in _SPLIT.split(text) if t.strip(" .")]


def block(title, text=None, topics=None, groups=None, note=None):
    b = {"title": title}
    if groups:
        b["groups"] = groups
    else:
        b["topics"] = topics if topics is not None else T(text)
    if note:
        b["note"] = note
    return b


# ---------------------------------------------------------------------------
# SHARED SYLLABUS BLOCKS
# ---------------------------------------------------------------------------
BLOCKS = {
    # --- End-user -----------------------------------------------------------
    "windows": block("Windows", "Computer Fundamentals - Introduction to OS/GUI - Wordpad - Notepad - Paintbrush - Windows Explorer - Control Panel."),
    "word": block("Word", "Creating Text and Documents - Indexes and Tables - Embedding Picture - Table Manipulation - Mail Merge - Macro."),
    "excel": block("Excel", "Formatting Cells - Charts - Pivot table - Data Table - Forms - Scenarios - Goal seek - Macros and Modules."),
    "powerpoint": block("PowerPoint", "Creating Presentations - OLE - Enhancing Presentation - Adding Audio & Video - Special Effects."),
    "internet_full": block("Internet", "Introduction to Internet, www, http & E-mail - Creating E-mail ID - Receiving & Sending E-mail - Chatting - Locating Information - Downloading."),
    "internet": block("Internet", "Creating E-mail ID - Receiving & Sending E-mail - Chatting - Locating Information - Downloading."),

    # --- Programming languages ---------------------------------------------
    "c": block("\u201cC\u201d Language", "Data Types - Operators - Expressions - Conditional Compilation - Looping & Branching - Arrays - Functions - Storage Classes - Structures and Unions - Pointers - Dynamic Memory Allocation - File Handling - Linked Lists - Double Linked List - Circular Linked List - Bit Manipulation - Introduction to Data Structure."),
    "cpp": block("OOPS Using C++", "Introduction to OOPS - Input & Output Streams - Classes & Objects - Member Functions - Function Overloading - Friend Functions & Classes - Operator Overloading - Constructor & Destructor - Inheritance - Polymorphism - File handling using Stream Classes - Instance - Templates."),
    "python": block("Python", groups=[
        ("Getting started", T("Introduction to Python - History - Features - Working with Python - Basic Syntax - Variable and Data Types - Operator and Expressions")),
        ("Conditions & loops", T("Conditional Statements - If - If-else - Nested if-else - Looping - For - While - Nested loops - Control Statements - Break - Continue - Pass")),
        ("Strings", T("String Manipulation - Accessing Strings - Basic Operations - String slices - Function and Methods")),
        ("Lists", T("Introduction - Accessing list - Operations - Working with lists - Function and Methods")),
        ("Tuples", T("Introduction - Accessing tuples - Operations - Working - Functions and Methods")),
        ("Dictionaries", T("Introduction - Accessing values in dictionaries - Working with dictionaries - Properties - Functions")),
        ("Functions", T("Defining a function - Calling a function - Types of functions - Function Arguments - Anonymous functions - Global and local variables")),
        ("Modules & packages", T("Modules - Importing module - Math module - Random module - Packages - Composition")),
        ("Input-Output & files", T("Input-Output - Printing on screen - Reading data from keyboard - Opening and closing file - Reading and writing files")),
        ("Exceptions", T("Functions - Exception Handling - Exception - Except clause")),
        ("Object-oriented Python", T("OOPs concept - Class and object - Attributes - Inheritance - Overloading - Overriding - Data hiding - Polymorphism - Data Structure")),
    ]),
    "python_short": block("Python", "Introduction - Conditional Statements - Looping - Control Statements - String Manipulation - Lists - Tuple - Dictionaries - Functions - Modules - Input/Output - Exception Handling - Files - Packages - OOPS Concept - Class and object - Inheritance - Polymorphism - Data Structure - MySQL Database Access - GUI Programming (Tkinter) - Image Processing in Python with Pillow & OPENCV."),
    "python_basic": block("Python", "Basic syntax and data types - Control flow - Functions and modules - File handling - Exception handling - List comprehensions and lambda functions - Object-oriented programming (OOP) concepts"),
    "python_adv": block("Advanced Python Programming", topics=["MySQL Database Access", "GUI Programming (Tkinter)", "Image Processing in Python with Pillow & OPENCV", "Web Scraping"]),
    "java": block("Java", "Data Types - Arrays - Functions - Classes - Methods - Inheritance - Polymorphism - Interfaces - Packages - Garbage Collection - Exception Handling - Data Structures - Collection - Generics - File Streams - Serialization - Multi Threading - Networking - Socket Programming - JDBC - JFC / Swing"),
    "core_java": block("Core Java", "Data Types - Arrays - Classes - Inheritance - Polymorphism - Abstraction - Packages - Exception - File Streams."),
    "html_basic": block("HTML", "Tags - Links - Anchors - Adding Pictures - Lists - Tables - Frames - Forms - Menu Controls."),

    # --- Front-end ----------------------------------------------------------
    "html5": block("HTML5", "HTML Basics - New Elements - Canvas - Multimedia - Form Elements, Semantic."),
    "css3": block("CSS3", "Syntax - Id, Class, Tag Styling - Using Text - Fonts - Links - Lists and Tables - Box Model - Text Effects - Transition - Animations."),
    "bootstrap": block("Bootstrap", "Responsive layouts with Grids - Themes - Components - Building Forms."),
    "js": block("Advanced JavaScript", "Basics, Arrays - Functions and Objects - DOM Model - Event Handling - Arrow Functions - Closures - Array Filter and Array Reduce - Regular Expression - OOPs - Promises - Async/Wait."),
    "react": block("React JS", "Creating an app - Using Templates - Components - Working with Props and State - Event Handling - Routing - Hooks - useState - useEffect - useRef - useCallback - useContext - Server Integration with API calls."),
    "html5_mern": block("HTML5", "HTML Basics - Semantic Elements - Document Meta Data - Canvas - Semantic Forms - Drag & Drop - HTML5 Validation"),
    "css3_mern": block("CSS3", "Selectors - Box Model - Layouts - Typography - Text Effects - Transition - Animations - Variable Properties."),
    "bootstrap_mern": block("Bootstrap", "Grid System - Responsive Utilities - Typography - Navs - Components - Forms & input Groups."),
    "js_mern": block("Advanced JavaScript", "Basics - Arrays - Functions & Objects - DOM - Event Handling - JSON - Arrow Functions - Closures - Error Handling - Regular Expressions - OOP - Promises and Async/Await."),
    "react_mern": block("React JS", "JSX - Components - Component LifeCycle - State & Props - Event Handling - Conditional Rendering - Routing - Fetching Data - Hooks - Building and Deployment."),
    "angular": block("Angular JS", "Directives - Expressions and Data Binding - Controllers - Modules - Services - Filters - Routing - Forms & Events - Animations - Custom Directives - Deployment."),

    # --- Databases ----------------------------------------------------------
    "mysql": block("MySQL", "Client / Server Concepts - Relational Model - Data Definition Using SQL - Modify Tables - Using ALTER TABLE Queries, Add a Column, Add an Index, Add a Primary Key - INSERT and DELETE Queries - UPDATE Queries - Using Select Queries - SELECT, WHERE, LIMIT, ORDER BY, GROUP BY, JOIN - Constraints and Indexes - Views - Expressions - Grouping - Using Functions - Math Functions, Compare String values, Work with Dates - JOIN and Subqueries - Advanced MySQL Query Processing."),
    "mysql_short": block("MySQL", "Creating and modifying tables - Data manipulation (INSERT, UPDATE, DELETE) - Querying databases (SELECT, JOIN, GROUP BY) - Aggregation functions (SUM, AVG, COUNT) - JOIN and Subqueries"),
    "mongodb": block("MongoDB", "Introduction to NoSQL databases - CRUD operations - Data Indexing & Aggregation - Working with Unstructured Data."),

    # --- Back-end / frameworks ---------------------------------------------
    "php": block("PHP", "PHP Basics - Syntax, Data Types, Variables, Constants, Operators and Expressions, Control Structures - Functions - Returning Values, Variable Scope - Arrays - Operations, Iteration, Sorting Array - Security - Formatting and Manipulating Strings with PHP - Web Programming - Forms and URLs, HTTP Headers, Sessions - Session Security - Using Date and Time Function - Working with Forms."),
    "laravel": block("Laravel", "Getting Started - Routing - Controllers - Forms & Request - Views - Redirection - Session & Cookie - Database - Authentication - Eloquent ORM - Rest API CRUD."),
    "node": block("Node JS", "Node Package Manager (NPM) - CommonJS Modules - File System - HTTP Module."),
    "express": block("Express JS", "Basics - Routing - Middleware - Template Engine - Handling Forms & Uploads - Database Integration - Authentication & Authorization - RESTful API - Error Handling - Deployment."),
    "spring": block("Spring Boot", "Spring Boot Annotations - CRUD Operations - Spring Data JPA - CrudRepository & JpaRepository - findBy methods in JPA - Custom Queries in JPA - Forms Development - Hibernate - JAVA REST API - REST API Media Types - Exception Handling - Connecting Spring Boot and React."),
    "django": block("Django", "What Is a Web Framework - The MVT Design Pattern - Django template tags - If/else - If/elif/else - For - Comments - Filters - Using templates to display data in the site - Forms Creation - CRUD operations - The Form class - Processing the form - Widgets - Validation - Forms in templates - Using Models and ORM - Building Web APIs using Django REST - Generic Views in Django Rest - Serializers - Working with Images - Authentication with tokens - Postman - Related models - Contenttypes app."),
    "git": block("Git", "Setting up a GIT repository - Version Control - Branching & Merging - Collaboration."),

    # --- Data & AI ----------------------------------------------------------
    "numpy": block("NumPy", "Arrays and array operations - Indexing and slicing - Mathematical functions - Linear algebra operations - Random module - Broadcasting."),
    "pandas": block("Pandas", "Series and DataFrame - Indexing and selecting data - Data cleaning and manipulation - Merging and joining data - Grouping and aggregating data - Handling missing data - Time series data"),
    "matplotlib": block("Matplotlib", "Basic plotting (line plots, scatter plots, bar plots) - Customizing plots (labels, titles, legends) - Multiple subplots - Histograms and box plots - 3D plotting."),
    "sklearn": block("Scikit-learn", "Data preprocessing - Model selection and evaluation - Supervised learning algorithms (e.g., regression, classification) - Unsupervised learning algorithms (e.g., clustering, dimensionality reduction) - Pipelines"),
    "tensorflow": block("TensorFlow & Keras", "Basics of neural networks - CNN - RNN - NLP - Building and training simple models - Layers and activation functions - Loss functions and optimizers - Model evaluation and validation - Transfer learning."),
    "excel_analytics": block("Excel", "Introduction - Formatting Worksheet - Conditional formatting - Pivot tables and charts - Formulas and functions (VLOOKUP, INDEX-MATCH, SUMIF, etc.) - Data cleaning and transformation - Data validation and sorting - Macros - Excel VBA and User Forms - Connect with External Data - Creating an Automation Project"),
    "powerbi": block("Power BI", "Connecting to data sources - Data transformation and cleaning - Building visualizations (charts, tables, maps) - Creating dashboards - Applying filters and slicers - Implementing advanced analytics in Power BI."),

    # --- Excel / VBA / marketing / AI --------------------------------------
    "adv_excel": block("Advanced Excel", "Introduction to MS Excel and Understanding Basic Working with it - Formatting Worksheet - Working with Formulas/Functions (Lookup and Reference Functions, Logical Function, Database Functions, Date and Time Functions, Information Functions, Math and Trigonometry Functions, Statistical Functions, Text Functions) - Conditional Formatting - Connect to other Database - Data Sorting and Filtering - Pivot Tables & Charts."),
    "vba": block("VBA Programming", "VBA Overview - VBA Programming Variables - Conditional Logic - String and String Functions - Programming Loops - Programming Arrays - Subs and Functions - Creating your first Macro - Excel VBA - Excel Objects - Excel Events - Excel VBA Error Handling - Excel VBA and User forms - Connect with an external data - Work on automation project."),
    "digital_marketing": block("Digital Marketing", "Introduction to Digital Marketing - Traditional vs Digital Marketing - Organic vs Inorganic Marketing - Content Creation - Graphic Designing - Social Media Marketing - Facebook - Instagram - Youtube - Search Marketing - Google Ads - Google Analytics."),
    "chatgpt": block("ChatGPT", topics=[], note="ChatGPT is a free-to-use AI system. Use it for engaging conversations, gain insights, automate tasks, and witness the future of AI, all in one place."),

    # --- .NET ---------------------------------------------------------------
    "csharp": block("Programming in C#", "OOPS concepts - The .NET Framework - Methods and control statements - Arrays - Constructors, Destructors - Polymorphism - Inheritance and Interfaces - Exception Handling - Structures and Properties - File Input/Output - Multithreading Applications - Delegates - Collection and Generics."),
    "vbnet": block("VB.NET", "Intro to Visual Studio IDE - Fundamentals of VB.NET - Functions, Procedures and Properties - Advanced Features of VB.NET - Windows Forms and Controls - MDI Forms and Implementing Help Systems - Working with Dialog Boxes - Printing in Windows Forms - Accessing Data - Introduction to LINQ - Crystal Reports - Globalization and Localization - Working with components and Assemblies - Deploying and Configuring Applications - Windows Presentation Foundation."),
    "aspnet": block("ASP.NET", "Intro to Visual Studio and ASP.NET - Creating a Website - Working with HTML Controls, Web Server Controls, Validation Controls, DataSource Controls and Navigation Controls - Master Pages, Styles, Themes - State Management - Error and Exception Handling - Data Access - XML - User controls and Custom Controls - Caching Techniques and Globalization - Security - Membership and Profiles - Deploying Applications - AJAX - ASP.NET Web parts - Silverlight."),
    "adonet": block("ADO.NET", "Introduction to Database - DML - DCL - Data Centric Applications and ADO.NET - Connecting to Data Sources - Performing Connected Database Operations - Building DataSets - Reading and Writing XML with ADO.NET, Building DataSets from Existing Data Sources."),

    # --- TallyPrime ---------------------------------------------------------
    "tally_intro": block("Introduction to TallyPrime", "Principles of Accounting - 5 Steps - Maintaining Company Data - F11 Features, F12 Configure."),
    "tally_masters": block("Masters", topics=["Group", "Ledger", "Chart of accounts", "Stock Group", "Stock Category", "Unit of measurement", "Godown", "Stock Item"]),
    "tally_vouchers": block("Tally Vouchers", topics=["Accounting Vouchers", "Inventory Vouchers"]),
    "tally_reports": block("Reports", "Balance Sheet - P & L A/c - Ratio Analysis - Cash Flow, Fund flow Statements - Ageing Analysis - Movement Analysis."),
    "tally_adv_acc": block("Advanced Accounting", "Bill wise Details - Cost Centres and Cost Categories - Voucher Classes and Cost centre Classes - Multiple Currencies - Bank reconciliation - Interest Calculation - Budgets & Scenario - Job Costing."),
    "tally_adv_inv": block("Advanced Inventory", "Order Processing - Reorder Levels - Tracking Numbers - Batch wise Details - Additional cost Details - Bill of Materials - Price List."),
    "tally_admin": block("System Administration and Other Utilities", "Consolidation of Accounts - Tally vault - Security Control - Tally Audit - Back up and Restore - Split company Data - Export and Import of Data - ODBC Compliance."),
    "tally_pos": block("Point of Sales", "Predetermination of Invoice - Multi payment Modes - Small & Smart Bills - POS Sales Register."),
    "tally_lang": block("Multi Language", "Supporting OS - Translation or Transliteration - System & Phonetic Keyboard - Sourcing from other Software."),
    "tally_gst": block("Goods & Service Tax (GST)", "Accounting of Purchase or Sales returns - Inter State Trade Accounting - Accounting of Exempted Items - Accounting Purchases from Unregistered Dealers - Accounting Input Credit on Capital Goods - GST Computation & Forms."),
    "tally_tds": block("TDS & TCS", "Entry - Calculator - Reports - e Returns."),
    "tally_payroll": block("Payroll", "Introduction to Payroll - Configuring Tally for Payroll - Creation of Payroll Masters - Recording of attendance - Preparation of Payroll Vouchers based on attendance - Preparation of a Salary Disbursement Voucher - Payroll Reports (Pay slip, Pay Sheet, Payroll Statement, Payment Advice, Payroll Register, Attendance Sheet, Attendance Register) - Introduction to Provident Fund."),
    "tally_addon": block("Add-on Features", "WhatsApp Connect - Import from Excel - Dashboard."),
}

TALLY_FULL = [
    "tally_intro", "tally_masters", "tally_vouchers", "tally_reports",
    "tally_adv_acc", "tally_adv_inv", "tally_admin", "tally_pos",
    "tally_lang", "tally_gst", "tally_tds", "tally_payroll", "tally_addon",
]
CHATGPT_TEXT = BLOCKS["chatgpt"]["note"]


def sec(title, *keys, elective=None, project=None, blocks=None):
    """Build a syllabus section from block keys (plus optional extras)."""
    out = {"title": title, "blocks": [BLOCKS[k] for k in keys]}
    if blocks:
        out["blocks"].extend(blocks)
    if elective:
        out["elective"] = elective
    if project:
        out["project"] = project
    return out


GENERIC_PROJECT_PY = "Using Python students will develop web development, data science, desktop applications, and more."

# ---------------------------------------------------------------------------
# PROGRAMMES
# ---------------------------------------------------------------------------
PROGRAMS = [
    # 1 ---------------------------------------------------------------------
    {
        "slug": "dca-tally", "code": "DCA Tally", "level": "Diploma",
        "name": "Diploma in Computer Application (Tally)",
        "category": "Accounting & Office",
        "audience": "School Final / Diploma / B.Com / M.Com / MBA.",
        "prerequisites": "No prior Computer knowledge is required.",
        "objective": "Upon completion of this course the participant will have a thorough knowledge in Microsoft Office suite and TallyPrime.",
        "overview": "This course provides the participant the knowledge of MS-Office and Accounting which is the basic requirement of any organisation.",
        "tools": ["Microsoft Office", "TallyPrime", "ChatGPT"],
        "sections": [
            sec("End-User Application", "windows", "word", "excel", "powerpoint", "internet_full"),
            sec("TallyPrime", *TALLY_FULL),
        ],
        "projects": ["With our guidance, students will develop Financial Accounting System, Inventory control, etc."],
        "chatgpt": True,
    },
    # 2 ---------------------------------------------------------------------
    {
        "slug": "dca-programming", "code": "DCA Programming", "level": "Diploma",
        "name": "Diploma in Computer Application (Programming)",
        "category": "Programming",
        "audience": "School Final / Diploma / B.Sc. / M.Sc. / BCA / MCA / Engineering Student",
        "prerequisites": "No prior Computer knowledge is required.",
        "objective": "Upon completion of this course the participant will have a thorough knowledge in Microsoft Office suite and can create application using object oriented concept.",
        "overview": "This course provides the participant the knowledge of programming which is the basic requirement of any student to enter into the world of computer.",
        "tools": ["C++", "Python", "Microsoft Office"],
        "sections": [
            sec("End-User Application", "windows", "word", "excel", "powerpoint", "internet_full"),
            sec("Programming Tool \u2013 Elective I", "c", "cpp", elective="Elective I", project="Development of System / Graphical Utility."),
            sec("Programming Tool \u2013 Elective II", "python", "python_adv", elective="Elective II", project=GENERIC_PROJECT_PY),
        ],
        "projects": [],
        "chatgpt": True,
    },
    # 3 ---------------------------------------------------------------------
    {
        "slug": "adad", "code": "ADAD", "level": "Advanced Diploma",
        "name": "Advanced Diploma in Artificial Intelligence & Data Science",
        "category": "Data & AI",
        "audience": "School Final / Diploma / B.Sc / B.C.A / M.Sc / M.C.A / Engineering Students",
        "prerequisites": "Participants should have a very basic understanding of any of the programming languages is beneficial but not mandatory.",
        "objective": "The objective of this course is to provide participants with comprehensive understanding of Artificial Intelligence (AI) and Data Science concepts, tools, and techniques. The course aims to empower learners to apply these skills to solve real-world problems and make data-driven decisions.",
        "overview": "Participants will gain hands-on experience with popular tools and frameworks such as TensorFlow and scikit-learn. Through a combination of theoretical knowledge and practical exercises, learners will develop the skills necessary to excel in the dynamic fields of AI and Data Science.",
        "tools": ["Python", "NumPy", "Pandas", "scikit-learn", "TensorFlow"],
        "sections": [
            sec("Language Skills", "python_basic"),
            sec("Data Management", "mysql_short", "mongodb"),
            sec("Data Wrangling", "numpy", "pandas"),
            sec("Data Visualization", "matplotlib"),
            sec("Machine Learning", "sklearn"),
            sec("Deep Learning", "tensorflow"),
            sec("Code Management", "git"),
        ],
        "projects": [],
    },
    # 4 ---------------------------------------------------------------------
    {
        "slug": "adda", "code": "ADDA", "level": "Advanced Diploma",
        "name": "Advanced Diploma in Data Analytics",
        "category": "Data & AI",
        "audience": "Diploma / Any Graduate.",
        "prerequisites": "No prior coding experience is required.",
        "objective": "The objective of this Data Analytics and Visualization course is to provide participants with a solid foundation in data analytics. The course aims to equip learners with the skills needed to efficiently analyze and visualize data for effective decision-making",
        "overview": "Through hands-on exercises and practical examples, participants will develop a versatile skill set for data analytics and reporting.",
        "tools": ["Excel", "Power BI", "Python", "Pandas", "Matplotlib"],
        "sections": [
            sec("Data Management", "excel_analytics", "mysql_short", "mongodb"),
            sec("Data Visualization", "matplotlib", "powerbi"),
            sec("Language Skills", "python_basic"),
            sec("Data Wrangling", "numpy", "pandas"),
            sec("Code Management", "git"),
        ],
        "projects": [],
    },
    # 5 ---------------------------------------------------------------------
    {
        "slug": "dpfd", "code": "DPFD", "level": "Diploma",
        "name": "Diploma in PHP Full Stack Developer",
        "category": "Full Stack",
        "audience": "+2 / Graduate / Undergraduate interested in pursuing a career in Web Programming.",
        "prerequisites": "No programming experience is required, but a basic understanding of HTML will be helpful.",
        "objective": "Upon completion of the course, you will be in a position to develop efficient and user-friendly applications.",
        "overview": "PHP, as a scripting language has been very popular due to its simplicity, speed and scalability. There are a number of PHP frameworks that help make this language easier to adopt and among the most popular of these is Laravel - widely adopted due to its simple and elegant syntax that eases the development process and simplifies routing, authentication, caching through built in templates, libraries and MVC architecture.",
        "tools": ["HTML5", "CSS3", "Bootstrap", "React", "PHP", "Laravel", "MySQL", "MongoDB"],
        "sections": [
            sec("I. Front-End Language & Library", "html5", "css3", "bootstrap", "js", "react"),
            sec("II. Database Management System", "mysql", "mongodb"),
            sec("III. Scripting Language & Framework", "php", "laravel"),
            sec("Code Management", "git"),
        ],
        "projects": [],
    },
    # 6 ---------------------------------------------------------------------
    {
        "slug": "adms", "code": "ADMS", "level": "Advanced Diploma",
        "name": "Advanced Diploma in MERN / MEAN Stack",
        "category": "Full Stack",
        "audience": "Diploma / B.Sc / B.C.A / M.Sc / M.C.A / Engineering Students.",
        "prerequisites": "Basic programming concept.",
        "objective": "Upon completion of the course, you will understand the full web application life cycle. Advance Knowledge in HTML, CSS, Bootstrap. Mastering the UI Layer (React JS / ANGULAR JS), API Layer (Express JS and Node JS) and DB Layer (MongoDB, MySQL) with Industry leading MERN / MEAN technologies.",
        "overview": "MERN and MEAN stacks are widely used for web application development. The key distinction is that the MEAN stack employs Angular Js in the front-end structure, whereas the MERN stack employs React Js for the User Interface (UI).",
        "tools": ["MongoDB", "Express", "React / Angular", "Node.js"],
        "sections": [
            sec("I. Front-End Language & Library", "html5_mern", "css3_mern", "bootstrap_mern", "js_mern",
                blocks=[dict(BLOCKS["react_mern"], elective="Elective I"), dict(BLOCKS["angular"], elective="Elective II")]),
            sec("II. Database Management System", "mysql", "mongodb"),
            sec("III. Web Framework", "node", "express"),
            sec("Code Management", "git"),
        ],
        "projects": [],
    },
    # 7 ---------------------------------------------------------------------
    {
        "slug": "dfjd", "code": "DFJD", "level": "Diploma",
        "name": "Diploma in Full Stack Java Developer",
        "category": "Full Stack",
        "audience": "Diploma / Graduates / Engineering Students.",
        "prerequisites": "Basic knowledge of Computing.",
        "objective": "This course help participants to master both front-end and back-end Java technologies and accelerate their career as a full stack software developer",
        "overview": "A Java full stack web developer is a developer with extensive knowledge and expertise in full stack tools and frameworks that works with java. This Full Stack Java Developer course is designed to give you an essence of front-end, middleware, and back-end Java web developer technologies. You will learn to build an end-to-end application and store data using MySql / MongoDB.",
        "tools": ["React", "MongoDB", "Bootstrap", "Spring Boot"],
        "sections": [
            sec("Front-End Language & Library", "html5", "css3", "bootstrap", "js", "react"),
            sec("Language", "core_java"),
            sec("Database Management System", "mysql", "mongodb"),
            sec("Web Framework", "spring"),
            sec("Code Management", "git"),
        ],
        "projects": [],
    },
    # 8 ---------------------------------------------------------------------
    {
        "slug": "dfpd", "code": "DFPD", "level": "Diploma",
        "name": "Diploma in Full Stack Python Developer",
        "category": "Full Stack",
        "audience": "Diploma / Graduates / Engineering Students.",
        "prerequisites": "Python programming language is mandatory",
        "objective": "This course help the participants to understand from basic to advance level in the application of Python.",
        "overview": "Python Full Stack Developer course is designed for beginners and developers to specialize in building complete modern web sites with Front-End, Back-End and Web Framework technologies, Database Management Systems. With rapid development in technologies, Python Full Stack Developer professionals are in demand.",
        "tools": ["React", "JavaScript", "Django", "MongoDB"],
        "sections": [
            sec("Front-End Language & Library", "html5", "css3", "bootstrap", "js", "react"),
            sec("Database Management System", "mysql", "mongodb"),
            sec("Web Framework", "django"),
            sec("Code Management", "git"),
        ],
        "projects": [],
    },
    # 9 ---------------------------------------------------------------------
    {
        "slug": "hdfd", "code": "HDFD", "level": "Honours Diploma",
        "name": "Honours Diploma in Full Stack Developer",
        "category": "Full Stack",
        "audience": "School Final / Diploma / Graduates / Engineering",
        "prerequisites": "No prior Computer knowledge is required.",
        "objective": "After completing the program, you will be eligible for a variety of career opportunities and build your career in front-end developer, back-end developer, API, or full stack developer roles in organizations ranging from start-ups to Fortune 500 companies.",
        "overview": "This course is designed for beginners to specialize in program solving skills with Programming Languages and building the complete modern web sites with Front-End, Back-End and Web Framework technologies, Database Management Systems. Upon completion of this course, you are 100% fit for the campus placements.",
        "tools": ["Bootstrap", "Django", "Python", "MongoDB", "Spring Boot"],
        "sections": [
            sec("I. Programming Language", "c", "cpp", "java", "python_short"),
            sec("II. Front-End Language & Library", "html5", "css3", "bootstrap", "js", "react"),
            sec("III. Database Management System", "mysql", "mongodb"),
            sec("IV. Web Framework", blocks=[dict(BLOCKS["django"], elective="Elective I"), dict(BLOCKS["spring"], elective="Elective II")]),
        ],
        "projects": ["To enhance the skills of the Student as full-stack developer they are given web development projects like E-Commerce Website, Food Delivery App, Content Management System, Project Management Dashboard, etc."],
    },
    # 10 --------------------------------------------------------------------
    {
        "slug": "dotnet", "code": ".NET", "level": "Diploma",
        "name": "Diploma in .Net",
        "category": "Programming",
        "audience": "A fresh graduate engineer, MCA, M.Sc., B.Sc., BCA, Software professional.",
        "prerequisites": "Basic Programming knowledge is required.",
        "objective": "At the end of this course the candidate will acquire a deep knowledge in programming, object oriented model, WEB Programming and the enterprise application development.",
        "overview": "This course is designed to create a new tool in the Software Development using object oriented environment, which will step into the normal programming, Web Technology and the enterprise application. This course is for those who want to become a Software Developer in profession.",
        "tools": ["C#", "VB.NET", "ASP.NET", "ADO.NET"],
        "sections": [
            sec("Course Coverage", "csharp", "vbnet", "aspnet", "adonet"),
        ],
        "projects": ["Students will develop web based applications like online reservation, Online share trading, live website, etc. Academic project done in this course can be used as final year college project."],
    },
    # 11 --------------------------------------------------------------------
    {
        "slug": "hdca-tally", "code": "HDCA Tally", "level": "Honours Diploma",
        "name": "Honours Diploma in Computer Application (Tally)",
        "category": "Accounting & Office",
        "audience": "School final students / Graduates / Students pursuing a career in Computer.",
        "prerequisites": "No prior Computer knowledge is required.",
        "objective": "Upon completion of this course, the participant acquires the advantage in choosing his / her career as an Application Programmer, Computerised Accountant, Web Programmer.",
        "overview": "This course has been tailor made as per the software industry requirement. It is a stepping stone for those who aspire to be a software professional.",
        "notes": ["Students must do two projects using Tally Prime and VBA Excel."],
        "tools": ["CSS3", "MySQL", "HTML5", "TallyPrime", "VBA", "Advanced Excel"],
        "sections": [
            sec("I. End-User Application", "windows", "word", "excel", "powerpoint", "internet"),
            sec("II. Front-End Language & Library", "html5", "css3"),
            sec("III. Database Management System", "mysql"),
            sec("IV. Financial Accounting", *TALLY_FULL, project="Live simulated projects are given to students."),
            sec("V. Advanced Excel & VBA Programming", "adv_excel", "vba",
                project="Students are given projects using VBA Excel and it will be helpful to explore how to use VBA to automate different tasks or developing applications/ tools using VBA."),
            sec("VI. Digital Marketing", "digital_marketing"),
        ],
        "projects": [],
        "chatgpt": True,
    },
    # 12 --------------------------------------------------------------------
    {
        "slug": "hdca-programming", "code": "HDCA Programming", "level": "Honours Diploma",
        "name": "Honours Diploma in Computer Application (Programming)",
        "category": "Programming",
        "audience": "School final students / Graduates / Students pursuing a career in Computer.",
        "prerequisites": "No prior Computer knowledge is required.",
        "objective": "Upon completion of this course, the participant acquires the advantage in choosing his / her career as an Application Programmer, Create applications using object oriented programming concepts such as inheritance, polymorphism and virtual functions.",
        "overview": "This course has been tailor made as per the software industry requirement. It is a stepping stone for those who aspire to be a software professional.",
        "notes": ["Students must do two projects using C/C++ and Python."],
        "tools": ["CSS3", "Microsoft Office", "HTML5", "MySQL", "C++", "Python"],
        "sections": [
            sec("I. End-User Application", "windows", "word", "excel", "powerpoint", "internet"),
            sec("II. Front-End Language & Library", "html5", "css3"),
            sec("III. Database Management System", "mysql"),
            sec("IV. Programming Tools", "c", blocks=[dict(BLOCKS["cpp"], project="Development of System / Graphical Utility."), dict(BLOCKS["python"]), BLOCKS["python_adv"]],
                project=GENERIC_PROJECT_PY),
            sec("V. Digital Marketing", "digital_marketing"),
        ],
        "projects": [],
        "chatgpt": True,
    },
    # 13 --------------------------------------------------------------------
    {
        "slug": "dmo", "code": "DMO", "level": "Diploma",
        "name": "Diploma in MS-Office",
        "category": "Accounting & Office",
        "audience": "House Wife / Elders, Professionals, Executives, Secretaries and students.",
        "prerequisites": "",
        "objective": "Upon completion of this course, the participant will be an expert in using all Windows products and surfing the internet.",
        "overview": "This course is a complete office suite preparing documentations, making graphs, displaying statistics, giving presentations using the MS-Office package and will enable the participants to handle any office work independently using computers.",
        "tools": ["Windows", "Word", "Excel", "PowerPoint"],
        "sections": [
            sec("Windows", "windows"),
            sec("MS-Office", "word", "excel", "powerpoint"),
            sec("Internet", "internet"),
        ],
        "projects": [],
        "case_study": "A case study reflecting a real-time situation would be given to the students, so that it gives confidence for them to manage any office work independently using computers.",
    },
    # 14 --------------------------------------------------------------------
    {
        "slug": "ccae", "code": "CCAE", "level": "Certificate",
        "name": "Certificate Course in Advanced Excel",
        "category": "Accounting & Office",
        "audience": "BBA, MBA Students, Data Analyst, Auditor, BPOs, Call centres professionals, Data conversion technicians, Programmers.",
        "prerequisites": "",
        "objective": "Upon completion of this course, the participant will be an expert in advanced Excel features including macro programming and functions.",
        "overview": "This course helps in promoting Excel professionals in advanced stage.",
        "tools": ["Advanced Excel", "VBA"],
        "sections": [
            sec("Advanced Excel", "adv_excel"),
            sec("VBA Programming", "vba"),
        ],
        "projects": [],
    },
    # 15 --------------------------------------------------------------------
    {
        "slug": "adpp", "code": "ADPP", "level": "Advanced Diploma",
        "name": "Advanced Diploma in Python Programming",
        "category": "Programming",
        "audience": "Diploma / Graduates / Engineering Students.",
        "prerequisites": "Basic knowledge of Computing.",
        "objective": "Upon completion of this course, the participant will be in a position to create components for the net and integrate them.",
        "overview": "This course enables you with skills to do effective programming for internet applications. It teaches you advanced programming techniques for the internet.",
        "tools": ["C", "C++", "Python"],
        "sections": [
            sec("Course Coverage", "c", "cpp", "python", "python_adv"),
        ],
        "projects": [],
    },
    # 16 --------------------------------------------------------------------
    {
        "slug": "adjp", "code": "ADJP", "level": "Advanced Diploma",
        "name": "Advanced Diploma in Java Programming",
        "category": "Programming",
        "audience": "Diploma / Graduates / Engineering Students.",
        "prerequisites": "Basic knowledge of Computing.",
        "objective": "Upon completion of this course, the participant will be in a position to create components for the net and integrate them.",
        "overview": "This course enables you with skills to do effective programming for internet applications. It teaches you advanced programming techniques for the internet.",
        "tools": ["C", "C++", "HTML", "CSS3", "Java"],
        "sections": [
            sec("Course Coverage", "c", "cpp", "html_basic", "css3", "java"),
        ],
        "projects": ["Students will develop web based applications like online reservation, Online share trading, live website, etc., and will be in a position to create java components for the internet."],
    },
    # 17 --------------------------------------------------------------------
    {
        "slug": "tallyprime-cca", "code": "TallyPrime", "level": "Certificate",
        "name": "TallyPrime \u2013 Certified Computer Accountant (CCA)",
        "category": "Accounting & Office",
        "audience": "B.Com., M.Com., BCA., BCS., ICWA, CA, ACS, CFA, MBA, Accounting professional and +2 Students.",
        "prerequisites": "Basic knowledge in Accounting.",
        "objective": "Upon completion of this course the candidate will get exposed to all features of TallyPrime and to cater financial needs of any business organization.",
        "overview": "This course extensively covers TallyPrime with Live examples based on industrial verticals.",
        "facts_title": "Facts To Learn Tally in CSC",
        "facts": [
            "Trained more than 2.50 lakhs Tally students.",
            "Well structured Course Material with Exercise and Example.",
            "Live stimulated Accounting Management Projects.",
            "First ever Institute to teach TallyPrime with GST along with projects.",
        ],
        "tools": ["TallyPrime"],
        "sections": [sec("Course Coverage", *TALLY_FULL)],
        "projects": ["Live simulated projects are given to students."],
    },
]

# ---------------------------------------------------------------------------
# NETWORK / CREDENTIALS (prospectus cover + back page)
# ---------------------------------------------------------------------------
JOURNEY = [
    ("1986", "Journey begins", ""),
    ("1992", "25", "Centers"),
    ("2006", "200", "Centers"),
    ("2020", "360", "Centers"),
]

CREDENTIALS_INTRO = (
    "The curriculum has been designed by the ISO 9001 : 2015 certified committee with meticulous "
    "care, taking valuable inputs from Industries, Customers and Academia, which helps the students "
    "to easily shift to other computer platforms depending on the industrial needs from time to time."
)

CREDENTIALS = [
    "An alumnus base of over 50 Lakhs students.",
    "1,00,000 students are trained every year.",
    "ISO 9001: 2015 certified curriculum design and development process.",
    "Trained 1,00,000 Government officials",
    "Center in the vicinity of every 15 kms.",
    "Project based training.",
    "Well structured course material.",
    "Experienced & Knowledgeable faculties.",
    "Unlimited computer lab timing.",
]

GOVT_TRAINED = [
    "TAHDCO", "BSNL", "ITCOT", "ICDS", "MoRD", "TAMCO", "BC & MBC Welfare Dept.",
    "SJSRY", "TNEB", "Indian Bank", "Health Care Dept", "Magalir Thittam",
    "Revenue & Survey Dept",
]

PARTNERS = [
    "Tally India Pvt Ltd",
    "IBT Institute Pvt Ltd (Bank / SSC / Railways / TNPSC Coaching)",
    "Speak Easy English Training (P) Ltd.",
]

CATEGORIES = ["All", "Full Stack", "Programming", "Data & AI", "Accounting & Office"]

LEVEL_ORDER = ["Certificate", "Diploma", "Advanced Diploma", "Honours Diploma"]


def get_program(slug):
    for p in PROGRAMS:
        if p["slug"] == slug:
            return p
    return None


def topic_count(program):
    n = 0
    for s in program["sections"]:
        for b in s["blocks"]:
            if "groups" in b:
                n += sum(len(g[1]) for g in b["groups"])
            else:
                n += len(b.get("topics", []))
    return n


for _p in PROGRAMS:
    _p["topic_count"] = topic_count(_p)
    _p["module_count"] = sum(len(s["blocks"]) for s in _p["sections"])
