# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import json
import os
from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_JSON = os.path.join(BASE_DIR,"package.json")

info = json.load(open("package.json"))

long_description = open("README.md",encoding="utf-8").read()

setup(
    name=info["name"],
    version=info["version"],
    description=info["description"],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

    ],
    keywords=info["keywords"],
    author=info["author"],
    author_email=info["email"],
    url=info["url"],
    project_urls={"Source Code": "https://github.com/alexpdev/ebookatty"},
    license=info["license"],
    packages=find_packages(exclude=["tests", "env"]),
    include_package_data=True,
    python_requires=">=3.6",
    setup_requires=["setuptools"],
    zip_safe=False,
    test_suite="complete",
)
