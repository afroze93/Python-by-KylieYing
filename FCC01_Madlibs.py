# string concatenation (aka how to put string together)
# suppose we want to create a string that says "subscrive to _____ "
youtuber = "Kylie Ying"  # some string variable

# a few ways to do this
print("subscribe to " + youtuber)

print("subscribe to {}".format(youtuber))

print(f"subscribe to {youtuber}")

adj = input("Adjective: ")
verb1 = input("Verb: ")
verb2 = input("Verb: ")
famous_person = input("Famous Person: ")

madlib = f"Computer Programming is so {adj}! It makes me so excited \
    all the time because I love to {verb1}. Stay hydrated and {verb2} \
        Like you are {famous_person}"

print(madlib)
