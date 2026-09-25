def height_to_inches(height):
    feet, inches = height.split("'")
    feet = int(feet)
    inches = int(inches)
    return feet * 12 + inches

print(height_to_inches("6'5"))
print(height_to_inches("6'10"))
print(height_to_inches("7'4"))