# filename: draw_circle.py
import turtle

# Create a turtle screen
screen = turtle.Screen()

# Create a turtle named "circle_drawer"
circle_drawer = turtle.Turtle()

# Draw a circle with a radius of 100 units
circle_drawer.circle(100)

# Keep the window open until it is clicked
screen.exitonclick()