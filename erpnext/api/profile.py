from frappe.auth import LoginManager
import frappe

@frappe.whitelist(allow_guest=True)
def login():
    username = frappe.form_dict.get("username")
    password = frappe.form_dict.get("password")

    try:
        lm = LoginManager()
        lm.authenticate(username, password)
        lm.post_login()

        user = frappe.get_doc("User", frappe.session.user)

        # Buat key jika belum ada
        if not user.api_key:
            user.api_key = frappe.generate_hash(length=15)
            user.save(ignore_permissions=True)

        # Buat secret jika belum ada
        if not user.get_password("api_secret"):
            user.reset_api_key()

        api_secret = user.get_password("api_secret")

        # Role Profile and Role List
        roles_list = frappe.get_all("Has Role", {"parent": user.name}, ["role"])
        
        role_profile_name = None
        roles = []
        if roles_list:
            roles = [role.role for role in roles_list]

        return {
            "success": True,
            "email": user.email,
            "full_name": user.full_name,
            "username": user.username,
            "language": user.language,
            "role_profile_name": role_profile_name,
            "desk_theme": user.desk_theme,
            "roles": roles,
            "api_key": user.api_key,
            "api_secret": api_secret,
            "user": user.name,
        }

    except frappe.AuthenticationError:
        frappe.local.response.http_status_code = 401
        return {
            "success": False,
            "message": "Invalid username or password"
        }

# uses for get user logged in
@frappe.whitelist()
def get_user_profile():
    user = frappe.get_doc("User", frappe.session.user)
    return user.as_dict()

# uses for get employee information from user_id
@frappe.whitelist()
def get_employee_information(user_id=None):
    if not user_id:
        user_id = frappe.session.user
    employee = frappe.get_value("Employee", {"user_id": user_id}, ["employee_name", "designation", "department"])
    if not employee:
        return None
    return {
        "employee_name": employee[0],
        "designation": employee[1],
        "department": employee[2],
    }