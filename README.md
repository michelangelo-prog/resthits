# resthits

Application that provides simple REST API for radio hits using Python, Flask, PostgreSQL and Docker.

## resthits description

Resthits provides following methods:

- [GET] `/api/v1/hits` - displays a list of 20 hits sorted by date added

    Example response:
    
    ```
    [
        {
            id: <hitId>,
            title: <title>,
            titleUrl: <titleUrl>
        },
        {
            id: <hitId>,
            title: <title>,
            titleUrl: <titleUrl>
        }
    ]
    ```
  
- [GET] `/api/v1/hits/{title_url}` - displays details of single hit

    Example response:
    
    ```
    {
        id: <hitId>,
        title: <title>,
        titleUrl: <titleUrl>,
        createdAd: <createdAd>,
        artist: {
            id: <artistId>,
            firstName: <firstName>
            lastName: <lastName>
        }
    }
    ```
  
- [POST] `/api/v1/hits` - creates a new hit based on the submitted object: `artistId`, `title`. Fields `created_at`/`title_url`
    are created automatically
    
- [PUT] `/api/v1/hits/{title_url}` - updates hit, you can only update `artistId`, `title` and `titleUrl`, additionally the update fills out the` updated_at` field

- [DELETE] `/api/v1/hits/{title_url}` - removes selected hit

Application has two tables:
- `hits` (id, artist_id as foreign key, title, title_url, created_at, updated_at)
- `artists` (id, first_name, last_name, created_at)

## Quick Start

Review the set up guides to configure the app:

[setup-with-docker.md](setup-with-docker.md)
