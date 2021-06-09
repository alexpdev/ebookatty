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

with open(PACKAGE_JSON) as package_file:
    info = json.load(package_file)

with open("README.md",encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pybook_metadata",
    version=info["version"],
    description=info["description"],
    long_description=long_description,
    include_package_data=True,
    python_requires=">=3.6",
    keywords=info["keywords"],
    packages=find_packages(where='pybook_metadata'),
)
