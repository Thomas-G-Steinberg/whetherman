import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='whetherman',
     version='0.1.1',
     author="Tom Steinberg",
     description="CLI Weather Forecast",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     install_requires=['requests'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     py_modules=['whetherman'],
     entry_points={'console_scripts': ['whetherman = whetherman:main']},
 )
