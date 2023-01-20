# Spotify Wrapped Plus

A small script, which generates a Spotify Wrapped Plus ranking, based on all of your Spotify Wrapped playlists.

## Installation
To run the script locally, please first install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then, provide a Spotify client_id and secrte in a file called `.env` in the root directory of the project.
```
SPOTIPY_CLIENT_ID="<your_client_id>"
SPOTIPY_CLIENT_SECRET="<your_client_secret>"
SPOTIPY_REDIRECT_URI="http://127.0.0.1:9090"
```
## Usage
To run the script, simply execute the following command:
```bash
python3 main.py -u <spotify_username>
```

To change the amount of songs shown, use the `-t` flag. The default is 10.
```bash
python3 main.py -u <spotify_username> -t 20
```


## Roadmap
- [ ] Add support for searching for a specific song
- [ ] Add support for ranking artists
- [ ] Add support for ranking genres
- [ ] Add support for ranking albums
- [ ] Add support for creating a playlist with the top songs


## Contributing
If you find a bug or have a feature request, please open an issue. If you want to contribute, please open a pull request.

## License
Distribution is permitted under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)