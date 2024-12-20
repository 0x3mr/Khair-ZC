from flask import Flask, jsonify

class ResponseHandler:
    def handle(self, error):
        raise NotImplementedError("This method should be overridden in subclasses")

class CharityResponseHandler(ResponseHandler):
    def handle(self, action):
        return jsonify({"message": f"User has {action} a charity successfully.", "status": "success"})

class CampaignResponseHandler(ResponseHandler):
    def handle(self, action):
        return jsonify({"message": f"User has {action} a campaign successfully.", "status": "success"})

class CampaignAttendanceHandler(ResponseHandler):
    def handle(self, attended):
        if attended:
            return jsonify({"message": "You have successfully attended this campaign.", "status": "success"})
        return jsonify({"message": "You did not attend this campaign.", "status": "error"})

class LoginResponseHandler(ResponseHandler):
    def handle(self, result):
        messages = {
            "success": "Login successful.",
            "invalid": "Invalid credentials. Please try again.",
            "server_issue": "Server issue. Please try again later."
        }
        return jsonify({"message": messages.get(result, "Unknown login error."), "status": result})

class SignupResponseHandler(ResponseHandler):
    def handle(self, result):
        messages = {
            "success": "Sign-up successful.",
            "invalid_email": "Invalid email address. Email must be zewailian.",
            "invalid_password": "Invalid password. Password must include at least 1 capital case, 1 small case, 1 number, and be at least 7 characters long."
        }
        return jsonify({"message": messages.get(result, "Unknown sign-up error."), "status": result})

class SearchResponseHandler(ResponseHandler):
    def handle(self, result):
        if result == "success":
            return jsonify({"message": "Search completed successfully.", "status": "success"})
        elif result == "invalid_search":
            return jsonify({"message": "Invalid search input. Avoid using special characters.", "status": "error"})
        return jsonify({"message": "Unknown search error.", "status": "error"})

class AdminCampaignResponseHandler(ResponseHandler):
    def handle(self, action):
        return jsonify({"message": f"Admin has performed {action} on a campaign.", "status": "success"})

class AdminUserResponseHandler(ResponseHandler):
    def handle(self, action):
        return jsonify({"message": f"Admin has performed {action} on a user.", "status": "success"})

class ErrorProcessor:
    def __init__(self):
        self.error_map = {
            "charity_follow":          lambda:  CharityResponseHandler().handle("followed"),
            "charity_unfollow":        lambda:  CharityResponseHandler().handle("unfollowed"),
            "charity_register":        lambda:  CharityResponseHandler().handle("registered"),
            "charity_unregister":      lambda:  CharityResponseHandler().handle("unregistered"),
            "campaign_follow":         lambda:  CampaignResponseHandler().handle("followed"),
            "campaign_unfollow":       lambda:  CampaignResponseHandler().handle("unfollowed"),
            "campaign_register":       lambda:  CampaignResponseHandler().handle("registered"),
            "campaign_unregister":     lambda:  CampaignResponseHandler().handle("unregistered"),
            "campaign_attended":       lambda:  CampaignAttendanceHandler().handle(True),
            "campaign_not_attended":   lambda:  CampaignAttendanceHandler().handle(False),
            "login_success":           lambda:  LoginResponseHandler().handle("success"),
            "login_invalid":           lambda:  LoginResponseHandler().handle("invalid"),
            "login_server_issue":      lambda:  LoginResponseHandler().handle("server_issue"),
            "signup_success":          lambda:  SignupResponseHandler().handle("success"),
            "signup_invalid_email":    lambda:  SignupResponseHandler().handle("invalid_email"),
            "signup_invalid_password": lambda:  SignupResponseHandler().handle("invalid_password"),
            "search_success":          lambda:  SearchResponseHandler().handle("success"),
            "search_invalid":          lambda:  SearchResponseHandler().handle("invalid_search"),
            "admin_campaign_create":   lambda:  AdminCampaignResponseHandler().handle("create"),
            "admin_campaign_read":     lambda:  AdminCampaignResponseHandler().handle("read"),
            "admin_campaign_update":   lambda:  AdminCampaignResponseHandler().handle("update"),
            "admin_campaign_delete":   lambda:  AdminCampaignResponseHandler().handle("delete"),
            "admin_user_update":       lambda:  AdminUserResponseHandler().handle("update (points)"),
            "admin_user_delete":       lambda:  AdminUserResponseHandler().handle("delete (bad behaviour)")
        }

    def process_error(self, error):
        return self.error_map.get(error, lambda: jsonify({"message": "Unknown error.", "status": "error"}))()