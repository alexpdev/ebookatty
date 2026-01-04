#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent
DESCRIPTION = "Tool for extracting metadata from common ebook formats"
LONG_DESCRIPTION = (BASE_DIR / "README.md").read_text(encoding="utf-8")


setup(
    name="ebookatty",
    version="0.3.1",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
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
    keywords=["ebook", "metadata", "mobi", "epub"],
    author="alexpdev",
    author_email="alexpdev@protonmail.com",
    entry_points={"console_scripts": ["ebookatty = ebookatty.__main__:main"]},
    url="https://github.com/alexpdev/ebookatty",
    project_urls={"Source Code": "https://github.com/alexpdev/ebookatty"},
    license="GNU LGPL v3",
    packages=find_packages(exclude=["tests", "env"]),
    include_package_data=True,
    python_requires=">=3.6",
    zip_safe=False,
    test_suite="complete",
)
