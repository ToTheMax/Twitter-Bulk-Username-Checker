# Twitter Bulk Username Checker

Twitter is soon going to release the usernames of inactive accounts ([source1][1], [source2][2]).
This tool can be used to check whether twitter usernames / handles are available, have an inactive account or are already taken.

[1]: https://twitter.com/elonmusk/status/1601124219009409024
[2]: https://twitter.com/elonmusk/status/1587252368999153665

## Requirements

- Python3

## Usage

1. Replace the `TOKEN` on top of `checker.py` with [your own](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens)
2. Run the script

   ```
   usage: checker.py [-h] username_file

   positional arguments:
   username_file  Name of a text file that contains a list of usernames

   options:
   -h, --help     show this help message and exit
   ```


## Example
![example-gif](https://user-images.githubusercontent.com/21971014/208538360-5f9509de-14b0-4c30-8ea0-43f564caea58.gif)



## Trouble Shooting

- `Error: Too Many Requests`: too many api calls were made, wait a little for the timeout
- `Error: Unauthorized`: make sure you added a token which is not expired
