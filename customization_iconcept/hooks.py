app_name = "customization_iconcept"
app_title = "Customization"
app_publisher = "Frontier Softech"
app_description = "All Customization"
app_email = "info@frontiersoftech.com"
app_license = "mit"

# Apps
# ------------------
doc_events = {
    "Sales Invoice": {
        "before_insert": "customization_iconcept.naming_series.before_insert",
        "on_submit": "customization_iconcept.journal_from_sales.create_finance_lender_jv"
    },
    # "POS Invoice": {
    #     "before_save": "customization_iconcept.set_branch.before_save",
    #     "on_submit": "customization_iconcept.pos_entry_create_journal.create_journal_entry_for_pos"
    # },
    # "Sales Invoice": {
    #     "before_save": "customization_iconcept.set_branch.before_save",
    #     "on_submit": "customization_iconcept.pos_entry_create_journal.create_journal_entry_for_pos"
    # }
}

after_migrate = "customization_iconcept.install.after_install"
# doctype_js = {
#     "POS Invoice": "public/js/pos_reference_prompt.js",
#     "Sales Invoice": "public/js/pos_reference_prompt_sale.js"
# }

doctype_js = {
    "Purchase Order": "public/js/required_by.js"
}

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "customization_iconcept",
# 		"logo": "/assets/customization_iconcept/logo.png",
# 		"title": "Customization",
# 		"route": "/customization_iconcept",
# 		"has_permission": "customization_iconcept.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/customization_iconcept/css/customization_iconcept.css"
# app_include_js = "/assets/customization_iconcept/js/customization_iconcept.js"

# include js, css files in header of web template
# web_include_css = "/assets/customization_iconcept/css/customization_iconcept.css"
# web_include_js = "/assets/customization_iconcept/js/customization_iconcept.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "customization_iconcept/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "customization_iconcept/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "customization_iconcept.utils.jinja_methods",
# 	"filters": "customization_iconcept.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "customization_iconcept.install.before_install"
# after_install = "customization_iconcept.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "customization_iconcept.uninstall.before_uninstall"
# after_uninstall = "customization_iconcept.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "customization_iconcept.utils.before_app_install"
# after_app_install = "customization_iconcept.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "customization_iconcept.utils.before_app_uninstall"
# after_app_uninstall = "customization_iconcept.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "customization_iconcept.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"customization_iconcept.tasks.all"
# 	],
# 	"daily": [
# 		"customization_iconcept.tasks.daily"
# 	],
# 	"hourly": [
# 		"customization_iconcept.tasks.hourly"
# 	],
# 	"weekly": [
# 		"customization_iconcept.tasks.weekly"
# 	],
# 	"monthly": [
# 		"customization_iconcept.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "customization_iconcept.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "customization_iconcept.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "customization_iconcept.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["customization_iconcept.utils.before_request"]
# after_request = ["customization_iconcept.utils.after_request"]

# Job Events
# ----------
# before_job = ["customization_iconcept.utils.before_job"]
# after_job = ["customization_iconcept.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"customization_iconcept.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

