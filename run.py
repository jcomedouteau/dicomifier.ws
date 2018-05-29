import werkzeug
import dicomifier_ws

werkzeug.run_simple(
    "127.0.0.1", 5000, dicomifier_ws.Application.instance(), 
    use_debugger=True, use_reloader=True)
