class TestMethod():
    def TestA(self):
        return 'A'
        #return "The Lion says " + self

            # models.py
        """
    from django.db import models

    class Animal(models.Model):

        An animal that knows how to make noise

        # Create some animals
        >>> lion = Animal.objects.create(name="lion", sound="roar")
        >>> cat = Animal.objects.create(name="cat", sound="meow")

        # Make 'em speak
        >>> lion.speak()
        'The lion says "roar"'
        >>> cat.speak()
        'The cat says "meow"'

        name = models.CharField(max_length=20)
        sound = models.CharField(max_length=20)

        def speak(self):
            return 'The %s says "%s"' % (self.name, self.sound)
            url : http://web.mit.edu/~mkgray/afs/bar/afs/athena/activity/a/aiti/OldFiles/Scripts/Django-1.3/docs/topics/testing.txt
                    """