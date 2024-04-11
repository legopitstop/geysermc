from dataclasses import dataclass
from PIL import Image, ImageFile
from io import BytesIO
import requests

__version__ = "1.0.0"

API_ENDPOINT = "https://api.geysermc.org"
CDN_ENDPOINT = "https://cdn.geysermc.org"
DOWNLOAD_ENDPOINT = "https://download.geysermc.org"


@dataclass
class ConvertedSkin:
    hash: str
    is_steve: bool
    signature: str
    texture_id: str
    value: str

    @staticmethod
    def from_json(data):
        return ConvertedSkin(
            data["hash"],
            data["is_steve"],
            data["signature"],
            data["texture_id"],
            data["value"],
        )


@dataclass
class Link:
    bedrock_id: int
    java_id: str
    java_name: str
    last_name_update: int

    @staticmethod
    def from_json(data):
        return Link(
            data["bedrock_id"],
            data["java_id"],
            data["java_name"],
            data["last_name_update"],
        )


@dataclass
class RecentConvertedSkinRefrance:
    id: int
    texture_id: str

    @staticmethod
    def from_json(data):
        return RecentConvertedSkinRefrance(data["id"], data["texture_id"])


@dataclass
class RecentConvertedSkinList:
    data: list[RecentConvertedSkinRefrance]
    total_pages: int

    def __iter__(self):
        for x in self.data:
            yield x

    @staticmethod
    def from_json(data: dict):
        return RecentConvertedSkinList(
            [RecentConvertedSkinRefrance.from_json(i) for i in data["data"]],
            data["total_pages"],
        )


@dataclass
class Statistics:
    pre_upload_queue: dict
    upload_queue: dict

    @staticmethod
    def from_json(data):
        return Statistics(data["pre_upload_queue"], data["upload_queue"])


@dataclass
class UsernameProfile:
    id: str
    name: str

    @staticmethod
    def from_json(data):
        return UsernameProfile(data["id"], data["name"])


@dataclass
class Project:
    project_id: str
    project_name: str
    versions: list[str]

    def __iter__(self):
        for x in self.versions:
            yield x

    @staticmethod
    def from_json(data):
        return Project(data["project_id"], data["project_name"], data["versions"])


@dataclass
class ProjectVersion:
    project_id: str
    project_name: str
    version: str
    builds: list[int]

    def __iter__(self):
        for x in self.builds:
            yield x

    @staticmethod
    def from_json(data):
        return ProjectVersion(
            data["project_id"], data["project_name"], data["version"], data["builds"]
        )


@dataclass
class BuildChange:
    commit: str
    summary: str
    message: str

    @staticmethod
    def from_json(data: dict):
        return BuildChange(data["commit"], data["summary"], data["message"])


@dataclass
class Download:
    name: str
    sha256: str

    @staticmethod
    def from_json(data: dict):
        return Download(data["name"], data["sha256"])


@dataclass
class Build:
    build: int
    time: str
    channel: str
    promoted: bool
    changes: list[BuildChange]
    downloads: dict[str, Download]

    @staticmethod
    def from_json(data: dict):
        downloads = {}
        for k, v in data["downloads"].items():
            downloads[k] = Download.from_json(v)
        return Build(
            data["build"],
            data["time"],
            data["channel"],
            data["promoted"],
            [BuildChange.from_json(x) for x in data["changes"]],
            downloads,
        )


@dataclass
class BuildList:
    project_id: str
    project_name: str
    version: str
    builds: list[Build]

    def __iter__(self):
        for x in self.builds:
            yield x

    @staticmethod
    def from_json(data: dict):
        return BuildList(
            data["project_id"],
            data["project_name"],
            data["version"],
            [Build.from_json(x) for x in data["builds"]],
        )


@dataclass
class Schema:
    data: dict

    @staticmethod
    def from_json(data):
        return Schema(data)


@dataclass
class Info:
    title: str
    version: str

    @staticmethod
    def from_json(data):
        return Info(data["title"], data["version"])


@dataclass
class Server:
    url: str
    variables: dict

    @staticmethod
    def from_json(data):
        return Server(data["url"], data["variables"])


@dataclass
class Path:
    data: dict

    @staticmethod
    def from_json(data):
        return Path(data)


@dataclass
class OpenAPI:
    components: dict[str, dict[str, Schema]]
    info: Info
    openapi: str
    paths: dict[str, Path]
    security: list
    servers: list[Server]
    tags: list[str]

    @staticmethod
    def from_json(data):
        paths = {}
        for p, v in data["paths"].items():
            paths[p] = Path.from_json(v)
        components = {}
        for c, v in data["components"].items():
            components[c] = {}
            for s, vv in v.items():
                components[c][s] = Schema.from_json(vv)
        return OpenAPI(
            components,
            Info.from_json(data["info"]),
            data["openapi"],
            paths,
            data["security"],
            [Server.from_json(x) for x in data["servers"]],
            data["tags"],
        )


# API


def _get(endpoint, path, **kw):
    res = requests.get(endpoint + path, **kw)
    if res.status_code == 200:
        return res
    data = res.json()
    if "message" in data:
        raise Exception(repr(data["message"]))
    raise Exception(data)


def get_bedrock_link(xuid: int) -> Link | None:
    """
    Get linked Java account from Bedrock xuid

    :param xuid: Bedrock xuid
    :type xuid: int
    :return: Linked accounts or an empty object if there is no account linked
    :rtype: list
    """
    res = _get(API_ENDPOINT, f"/v2/link/bedrock/{xuid}").json()
    if "last_name_update" in res:
        return Link.from_json(res)
    return None


def get_java_link(uuid: str) -> list[Link]:
    """
    Get linked Bedrock account from Java UUID

    :param uuid: Java UUID
    :type uuid: str
    :return: Linked account or an empty object if there is no account linked
    :rtype: list
    """
    res = _get(API_ENDPOINT, f"/v2/link/java/{uuid}").json()
    return [Link.from_json(x) for x in res]


# TODO: illegal online link data, internal server error, received invalid tokens, The provided value for the 'code' parameter is not valid.
def verify_online_link(bedrock: str = None, java: str = None) -> list:
    payload = {}
    if bedrock:
        payload["bedrock"] = bedrock
    if java:
        payload["java"] = java
    return requests.post(API_ENDPOINT + f"/v2/link/online", json=payload).json()


def get_all_stats() -> Statistics:
    """
    Get all publicly available Global Api statistics

    :rtype: Statistics
    """
    res = _get(API_ENDPOINT, "/v2/stats").json()
    return Statistics.from_json(res)


def get_gamertag_batch(*xuids: str) -> dict[str, str]:
    return (
        requests.post(
            API_ENDPOINT + "/v2/xbox/batch/gamertag", json={"xuids": list(xuids)}
        )
        .json()
        .get("data", {})
    )


def get_gamertag(xuid: int) -> str:
    """
    Get the gamertag from a xuid

    :param xuid: The xuid of the Bedrock player
    :type xuid: int
    :return: The gamertag associated with the xuid or an empty object if there is account with the given xuid
    :rtype: str
    """
    return _get(API_ENDPOINT, f"/v2/xbox/gamertag/{xuid}").json()["gamertag"]


def get_xuid(gamertag: str) -> int:
    """
    Get the xuid from a gamertag

    :param gamertag: The gamertag of the Bedrock player
    :type gamertag: str
    :return: The xuid associated with the gamertag or an empty object if there is account with the given gamertag
    :rtype: int
    """
    return _get(API_ENDPOINT, f"/v2/xbox/xuid/{gamertag}").json().get("xuid")


def get_recent_uploads() -> RecentConvertedSkinList:
    """
    Get a list of the most recently uploaded skins

    :return: The most recently uploaded skins. First element has been uploaded most recently etc.
    :rtype: RecentConvertedSkinList
    """
    res = _get(API_ENDPOINT, "/v2/skin/bedrock/recent").json()
    return RecentConvertedSkinList.from_json(res)


def get_skin(xuid: int) -> ConvertedSkin | None:
    """
    Get the most recently converted skin of a Bedrock player

    :param xuid: Bedrock xuid
    :type xuid: int
    :return: Converted skin or an empty object if there is no skin stored for that player
    :rtype: ConvertedSkin
    """
    res = _get(API_ENDPOINT, f"/v2/skin/{xuid}").json()
    if "hash" in res:
        return ConvertedSkin.from_json(res)
    return None


def get_project_news(project: str) -> list:
    return _get(API_ENDPOINT, f"/v2/news/{project}").json()


def get_bedrock_or_java_uuid(username: str, prefix: str = ".") -> dict:
    """
    Utility endpoint to get either a Java UUID or a Bedrock xuid

    :param username: The username of the Minecraft player
    :type username: str
    :param prefix: The prefix used in your Floodgate config, defaults to "."
    :type prefix: str, optional
    :return: The Bedrock xuid in Floodgate UUID format and username. Response made to be identical to the Mojang endpoint
    :rtype: dict
    """
    return _get(
        API_ENDPOINT, f"/v2/utils/uuid/bedrock_or_java/{username}?prefix={prefix}"
    ).json()


def get_openapi() -> OpenAPI:
    res = _get(API_ENDPOINT, "/openapi").json()
    return OpenAPI.from_json(res)


# DOWNLOAD


def get_projects() -> list[str]:
    """
    Gets a list of all available projects.

    :return: All available projects.
    :rtype: list[str]
    """
    return _get(DOWNLOAD_ENDPOINT, "/v2/projects").json()["projects"]


def get_project(project: str) -> Project:
    """
    Gets information about a project.

    :param project: The project identifier.
    :type project: str
    :rtype: Project
    """
    res = _get(DOWNLOAD_ENDPOINT, f"/v2/projects/{project}").json()
    return Project.from_json(res)


def get_version(project: str, version: str = "latest") -> ProjectVersion:
    """
    Gets information about a version.

    :param project: The project identifier.
    :type project: str
    :param version: A version of the project., defaults to "latest"
    :type version: str, optional
    :rtype: ProjectVersion
    """
    res = _get(DOWNLOAD_ENDPOINT, f"/v2/projects/{project}/versions/{version}").json()
    return ProjectVersion.from_json(res)


def get_version_builds(project: str, version: str = "latest") -> BuildList:
    """
    Gets all available builds for a project's version.

    :param project: The project identifier.
    :type project: str
    :param version: A version of the project., defaults to "latest"
    :type version: str, optional
    :rtype: BuildList
    """
    res = _get(
        DOWNLOAD_ENDPOINT, f"/v2/projects/{project}/versions/{version}/builds"
    ).json()
    return BuildList.from_json(res)


def get_build(project: str, version: str = "latest", build: str = "latest") -> Build:
    """
    Gets information related to a specific build.

    :param project: The project identifier.
    :type project: str
    :param version: A version of the project., defaults to "latest"
    :type version: str, optional
    :param build: A build of the version., defaults to "latest"
    :type build: str, optional
    :rtype: Build
    """
    res = _get(
        DOWNLOAD_ENDPOINT, f"/v2/projects/{project}/versions/{version}/builds/{build}"
    ).json()
    return Build.from_json(res)


def get_download(
    project: str, download: str, version: str = "latest", build: int | str = "latest"
) -> bytes:
    """
    Downloads the given file from a build's data.

    :param project: The project identifier.
    :type project: str
    :param download: A download of the build.
    :type download: str
    :param version: A version of the project., defaults to "latest"
    :type version: str, optional
    :param build: A build of the version., defaults to "latest"
    :type build: int | str, optional
    :rtype: bytes
    """
    return requests.get(
        DOWNLOAD_ENDPOINT
        + f"/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}",
        stream=True,
    ).content


# CDN


def get_raw_texture(texture_id: str) -> ImageFile.ImageFile:
    """
    get_raw_texture

    :param texture_id: Java texture id
    :type texture_id: str
    :rtype: ImageFile.ImageFile
    """
    res = _get(CDN_ENDPOINT, f"/render/raw/{texture_id}", stream=True)
    return Image.open(BytesIO(res.content))
