from flask import Flask, jsonify


class ResponseHandler:
    def handle(self, error):
        raise NotImplementedError(
            "This method should be overridden in subclasses")


class CharityResponseHandler(ResponseHandler):
    def handle(self, action):
        if action == "missing_fields":
            return {"message": "Missing required fields for the charity.", "status": "error"}
        if action == "invalid_input":
            return {"message": "Invalid input. Please provide a valid charity.", "status": "error"}
        if action == "exists":
            return {"message": "Charity with the same name already exists.", "status": "error"}
        if action == "id_exists":
            return {"message": "Charity with the same ID already exists.", "status": "error"}
        if action == "id_required":
            return {"message": "Charity ID is required.", "status": "error"}
        if action == "not_found":
            return {"message": "Charity not found.", "status": "error"}
        if action == "already_following_charity":
            return {"message": "User is already following this charity.", "status": "error"}
        return {"message": f"User has {action} a charity successfully.", "status": "success"}

class PasswordResponseHandler(ResponseHandler):
    def handle(self, action):
        messages = {
            "email_missing": "Email is required to reset the password.",
            "user_not_found": "No user found with the provided email address.",
            "reset_invalid_data": "Invalid data provided for password reset.",
            "reset_invalid_password": "Invalid password. It must include at least 1 letter, 1 number, and be at least 7 characters long.",
            "reset_token_expired": "The password reset token has expired.",
            "reset_token_invalid": "The password reset token is invalid.",
            "password_reset_success": "Password has been reset successfully.",
            "change_invalid_data": "Invalid data provided for changing the password.",
            "password_incorrect": "The current password is incorrect.",
            "password_change_success": "Password has been changed successfully."
        }
        status = "success" if "success" in action else "error"
        return {"message": messages.get(action, "Unknown password error."), "status": status}


class CampaignResponseHandler(ResponseHandler):
    def handle(self, action):
        if action == "camp_not_found":
            return {"message": "Campaign not fonud.", "status": "error"}
        if action == "camp_id_missing":
            return {"message": "Campaign ID is required.", "status": "error"}
        if action == "camp_full":
            return {"message": "Campaign is full. Cannot register.", "status": "error"}
        if action == "removal_success":
            return {"message": "Campaign removed successfully.", "status": "success"}
        return {"message": f"User has {action} a campaign successfully.", "status": "success"}


class CampaignAttendanceHandler(ResponseHandler):
    def handle(self, attended):
        if attended == "camp_attend":
            return {"message": "You have successfully attended this campaign.", "status": "success"}
        return {"message": "You did not attend this campaign.", "status": "error"}


class LoginResponseHandler(ResponseHandler):
    def handle(self, result):
        messages = {
            "success": "Login successful.",
            "invalid": "Invalid credentials. Please try again.",
            "server_issue": "Server issue. Please try again later."
        }
        return {"message": messages.get(result, "Unknown login error."), "status": result}


class SignupResponseHandler(ResponseHandler):
    def handle(self, result):
        messages = {
            "success": "Sign-up successful.",
            "invalid_email": "Invalid email address. Email must be zewailian.",
            "invalid_password": "Invalid password. Password must include at least 1 capital case, 1 small case, 1 number, and be at least 7 characters long."
        }
        return {"message": messages.get(result, "Unknown sign-up error."), "status": result}


class SearchResponseHandler(ResponseHandler):
    def handle(self, result):
        if result == "success":
            return {"message": "Search completed successfully.", "status": "success"}
        elif result == "invalid_search":
            return {"message": "Invalid search input. Avoid using special characters.", "status": "error"}
        return {"message": "Unknown search error.", "status": "error"}


class AdminCampaignResponseHandler(ResponseHandler):
    def handle(self, action):
        return {"message": f"Admin has performed {action} on a campaign.", "status": "success"}


class AdminUserResponseHandler(ResponseHandler):
    def handle(self, action):
        return jsonify({"message": f"Admin has performed {action} on a user.", "status": "success"})


class UserResponseHandler(ResponseHandler):
    def handle(self, found):
        if found == "user_id_required":
            return {"message": "User ID is required.", "status": "error"}
        if found == "user_found":
            return {"message": "User found successfully.", "status": "success"}
        if found == "user_already_registered":
            return {"message": "User is already registered.", "status": "error"}
        if found == "user_not_registered":
            return {"message": "User is not registered.", "status": "error"}
        return {"message": "User not found.", "status": "error"}


class ShopResponseHandler:
    def __init__(self):
        self.messages = {
            "no_products": "No products found in the shop.",
            "missing_fields": "Missing required fields for the product.",
            "invalid_price": "Invalid price. It must be a positive number.",
            "duplicate_product": "Product with the same name already exists.",
            "product_added": "Product added successfully to the shop.",
            "add_product_error": "An error occurred while adding the product."
        }

    def handle(self, action):
        if action not in self.messages:
            return jsonify({"message": "Unknown shop error.", "status": "error"})

        status = "success" if "added" in action or action == "product_added" else "error"
        return jsonify({"message": self.messages[action], "status": status})


class ErrorProcessor:
    def __init__(self):
        self.error_map = {
            "charity_follow":            lambda:  CharityResponseHandler().handle("followed"),
            "charity_unfollow":          lambda:  CharityResponseHandler().handle("unfollowed"),
            "charity_register":          lambda:  CharityResponseHandler().handle("registered"),
            "charity_unregister":        lambda:  CharityResponseHandler().handle("unregistered"),
            "charity_invalid_input":     lambda:  CharityResponseHandler().handle("invalid_input"),
            "charity_missing_fields":    lambda:  CharityResponseHandler().handle("missing_fields"),
            "charity_exists":            lambda name:  CharityResponseHandler().handle("exists"),
            "charity_id_exists":         lambda id:  CharityResponseHandler().handle("id_exists"),
            "charity_id_required":       lambda:  CharityResponseHandler().handle("id_required"),
            "charity_not_found":         lambda:  CharityResponseHandler().handle("not_found"),
            "already_following_charity": lambda:  CharityResponseHandler().handle("already_following_charity"),
            "campaign_follow":           lambda:  CampaignResponseHandler().handle("followed"),
            "campaign_unfollow":         lambda:  CampaignResponseHandler().handle("unfollowed"),
            "campaign_register":         lambda:  CampaignResponseHandler().handle("registered"),
            "campaign_unregister":       lambda:  CampaignResponseHandler().handle("unregistered"),
            "campaign_attended":         lambda:  CampaignAttendanceHandler().handle("camp_attend"),
            "campaign_not_attended":     lambda:  CampaignAttendanceHandler().handle("camp_not_attend"),
            "campaign_not_found":        lambda:  CampaignResponseHandler().handle("camp_not_found"),
            "campaign_id_missing":       lambda:  CampaignResponseHandler().handle("camp_id_missing"),
            "campaign_full":             lambda:  CampaignResponseHandler().handle("camp_full"),
            "removal_success":           lambda:  CampaignResponseHandler().handle("removal_success"),
            "login_success":             lambda:  LoginResponseHandler().handle("success"),
            "login_invalid":             lambda:  LoginResponseHandler().handle("invalid"),
            "login_server_issue":        lambda:  LoginResponseHandler().handle("server_issue"),
            "signup_success":            lambda:  SignupResponseHandler().handle("success"),
            "signup_invalid_email":      lambda:  SignupResponseHandler().handle("invalid_email"),
            "signup_invalid_password":   lambda:  SignupResponseHandler().handle("invalid_password"),
            "search_success":            lambda:  SearchResponseHandler().handle("success"),
            "search_invalid":            lambda:  SearchResponseHandler().handle("invalid_search"),
            "admin_campaign_create":     lambda:  AdminCampaignResponseHandler().handle("create"),
            "admin_campaign_read":       lambda:  AdminCampaignResponseHandler().handle("read"),
            "admin_campaign_update":     lambda:  AdminCampaignResponseHandler().handle("update"),
            "admin_campaign_delete":     lambda:  AdminCampaignResponseHandler().handle("delete"),
            "admin_user_update":         lambda:  AdminUserResponseHandler().handle("update (points)"),
            "admin_user_delete":         lambda:  AdminUserResponseHandler().handle("delete (bad behaviour)"),
            "shop_no_products":          lambda:  ShopResponseHandler().handle("no_products"),
            "shop_missing_fields":       lambda:  ShopResponseHandler().handle("missing_fields"),
            "shop_invalid_price":        lambda:  ShopResponseHandler().handle("invalid_price"),
            "shop_duplicate_product":    lambda:  ShopResponseHandler().handle("duplicate_product"),
            "shop_product_added":        lambda:  ShopResponseHandler().handle("product_added"),
            "shop_add_product_error":    lambda:  ShopResponseHandler().handle("add_product_error"),
            "user_found":                lambda:  UserResponseHandler().handle("user_found"),
            "user_not_found":            lambda:  UserResponseHandler().handle("user_not_found"),
            "user_id_required":          lambda:  UserResponseHandler().handle("user_id_required"),
            "user_already_registered":   lambda:  UserResponseHandler().handle("user_already_registered"),
            "user_not_registered":       lambda:  UserResponseHandler().handle("user_not_registered"),
            "campaign_follow":           lambda:  CampaignResponseHandler().handle("followed"),
            "campaign_unfollow":         lambda:  CampaignResponseHandler().handle("unfollowed"),
            "campaign_register":         lambda:  CampaignResponseHandler().handle("registered"),
            "campaign_unregister":       lambda:  CampaignResponseHandler().handle("unregistered"),
            "campaign_attended":         lambda:  CampaignAttendanceHandler().handle("camp_attend"),
            "campaign_not_attended":     lambda:  CampaignAttendanceHandler().handle("camp_not_attend"),
            "campaign_not_found":        lambda:  CampaignResponseHandler().handle("camp_not_found"),
            "login_success":             lambda:  LoginResponseHandler().handle("success"),
            "login_invalid":             lambda:  LoginResponseHandler().handle("invalid"),
            "login_server_issue":        lambda:  LoginResponseHandler().handle("server_issue"),
            "signup_success":            lambda:  SignupResponseHandler().handle("success"),
            "signup_invalid_email":      lambda:  SignupResponseHandler().handle("invalid_email"),
            "signup_invalid_password":   lambda:  SignupResponseHandler().handle("invalid_password"),
            "email_missing":             lambda:  PasswordResponseHandler().handle("email_missing"),
            "user_not_found":            lambda:  PasswordResponseHandler().handle("user_not_found"),
            "reset_invalid_data":        lambda:  PasswordResponseHandler().handle("reset_invalid_data"),
            "reset_invalid_password":    lambda:  PasswordResponseHandler().handle("reset_invalid_password"),
            "reset_token_expired":       lambda:  PasswordResponseHandler().handle("reset_token_expired"),
            "reset_token_invalid":       lambda:  PasswordResponseHandler().handle("reset_token_invalid"),
            "password_reset_success":    lambda:  PasswordResponseHandler().handle("password_reset_success"),
            "change_invalid_data":       lambda:  PasswordResponseHandler().handle("change_invalid_data"),
            "password_incorrect":        lambda:  PasswordResponseHandler().handle("password_incorrect"),
            "password_change_success":   lambda:  PasswordResponseHandler().handle("password_change_success"),
            "search_success":            lambda:  SearchResponseHandler().handle("success"),
            "search_invalid":            lambda:  SearchResponseHandler().handle("invalid_search"),
            "admin_campaign_create":     lambda:  AdminCampaignResponseHandler().handle("create"),
            "admin_campaign_read":       lambda:  AdminCampaignResponseHandler().handle("read"),
            "admin_campaign_update":     lambda:  AdminCampaignResponseHandler().handle("update"),
            "admin_campaign_delete":     lambda:  AdminCampaignResponseHandler().handle("delete"),
            "admin_user_update":         lambda:  AdminUserResponseHandler().handle("update (points)"),
            "admin_user_delete":         lambda:  AdminUserResponseHandler().handle("delete (bad behaviour)"),
            "shop_no_products":          lambda:  ShopResponseHandler().handle("no_products"),
            "shop_missing_fields":       lambda:  ShopResponseHandler().handle("missing_fields"),
            "shop_invalid_price":        lambda:  ShopResponseHandler().handle("invalid_price"),
            "shop_duplicate_product":    lambda:  ShopResponseHandler().handle("duplicate_product"),
            "shop_product_added":        lambda:  ShopResponseHandler().handle("product_added"),
            "shop_add_product_error":    lambda:  ShopResponseHandler().handle("add_product_error"),
            "user_found":                lambda:  UserResponseHandler().handle("user_found"),
            "user_not_found":            lambda:  UserResponseHandler().handle("user_not_found"),
            "user_id_required":          lambda:  UserResponseHandler().handle("user_id_required"),
        }

    def process_error(self, error, name=None, id=None):
        if id:
            return self.error_map.get(error)(id)
        if name:
            return self.error_map.get(error)(name)
        return self.error_map.get(error, lambda: jsonify({"message": "Unknown error.", "status": "error"}))()
