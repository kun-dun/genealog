from delphivcl import *
# Import your exported form
from iniform import Form3

# Initialize application
Application.Initialize()

# Create an instance of your form
myForm = Form3(Application)

# Connect custom event handlers if needed
def my_button_click(sender):
    myForm.Label1.Caption = "Button was clicked!"

myForm.Button1.OnClick = my_button_click

# Show and run
myForm.Show()
Application.Run()