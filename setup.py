# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import io
import json
import os
import subprocess
import sys

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PACKAGE_JSON = os.path.join(BASE_DIR,"package.json")
with open(PACKAGE_JSON) as package_file:
    version_string = json.load(package_file)["version"]

with io.open("README.md",encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ebook-metadata",
    description=("Tool for extracting metadata from common ebook formats"),
    long_description=long_description,
    version=version_string,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts":["ebook-metadata.cli"]},
    install_requires=[],
    python_requires="~3.6",
    author="alexpdev",
    author_email="alexpdev@protonmail.com",
    url="https://github.com/alexpdev",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
