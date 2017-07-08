class Foo(object):

	""" some Foo class """

	def bar(self, *args, **kwargs):
		for i in range(42):
			yield i
