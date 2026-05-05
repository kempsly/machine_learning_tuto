import sqlite3 

## connect to sqllite
connection=sqlite3.connect("student.db")

##create a cursor object to insert record,create table
cursor=connection.cursor()

## create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

# Insert multiple records

# ## Insert some more records
# cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
# cursor.execute('''Insert Into STUDENT values('John','Data Science','B',100)''')
# cursor.execute('''Insert Into STUDENT values('Mukesh','Data Science','A',86)''')
# cursor.execute('''Insert Into STUDENT values('Jacob','DEVOPS','A',50)''')
# cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')
# ----------------------------
students = [
    ('Krish','Data Science','A',90),
    ('John','Data Science','B',100),
    ('Mukesh','Data Science','A',86),
    ('Jacob','DEVOPS','A',50),
    ('Dipesh','DEVOPS','A',35),
    
    # NEW RECORDS
    ('Anita','Data Science','B',78),
    ('Rahul','Data Science','C',88),
    ('Sonia','DEVOPS','B',67),
    ('Karan','DEVOPS','C',45),
    ('Meena','Data Science','A',92),
    ('Alex','DEVOPS','A',73),
    ('Priya','Data Science','B',81),
    ('David','DEVOPS','B',60)
]

# insert all at once
cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", students)

# ----------------------------
# Display records
# ----------------------------
print("The inserted records are:\n")

data = cursor.execute("SELECT * FROM STUDENT")

for row in data:
    print(row)

# save changes
connection.commit()

# close connection
connection.close()