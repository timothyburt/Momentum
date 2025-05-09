# App Configuration File

class Device:
	@staticmethod
	def mobile():
		return {"app_width": 350, "app_height": 700, "app_resizable": False}

	@staticmethod
	def tablet():
		return {"app_width": 768, "app_height": 1024, "app_resizable": False}

	@staticmethod
	def web():
		return {"app_width": 1280, "app_height": 720, "app_resizable": True}

	@staticmethod
	def desktop():
		return {"app_width": 1920, "app_height": 1080, "app_resizable": True}

class Config:
	APP_TITLE = "Momentum App"  # App title
	APP_PADDING = 0  # App-wide padding
	APP_MARGIN = 0  # App-wide margin

	@staticmethod
	def get_device_dimensions(device_type):
		if device_type == "mobile":
			return Device.mobile()
		elif device_type == "tablet":
			return Device.tablet()
		elif device_type == "web":
			return Device.web()
		elif device_type == "desktop":
			return Device.desktop()
		else:
			raise ValueError("Invalid device type")

	# Initialize DEVICE after defining the method
	DEVICE = get_device_dimensions("mobile")
	APP_WIDTH = DEVICE["app_width"]
	APP_HEIGHT = DEVICE["app_height"]
	APP_RESIZABLE = DEVICE["app_resizable"]
