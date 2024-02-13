# import subprocess

# to_update = ['fonttools','ipykernel','ipython','jupyter_client','jupyter_core','keras','numpy','Pygments','setuptools']

# def update_library(library_name):
#     try:
#         subprocess.check_call(['pip', 'install', '--upgrade', '--user', library_name])
#         print(f'Successfully updated {library_name}.')
#     except subprocess.CalledProcessError as e:
#         print(f'Error updating {library_name}. Return code: {e.returncode}')

# # Example: Update 'requests' library
# for package in to_update:
#     update_library(package)
import math
print(math.gcd(0, 10, 5))