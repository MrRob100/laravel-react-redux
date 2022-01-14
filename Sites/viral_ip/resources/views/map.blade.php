<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7/leaflet.css" />
    <script src="http://cdn.leafletjs.com/leaflet-0.7/leaflet.js"></script>
    <script src="https://d3js.org/d3.v3.min.js" type="text/javascript"></script>
    <script src="{{ asset('js/app.js') }}" defer></script>
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">

    <style>
        html,
        body {
            height: 100%;
            width: 100%;
        }

        body {
            margin: 0;
        }

        #map, #app, .contain {
            width: 100%;
            height: 100%;
        }

    </style>
</head>

<body>
<div id="app">
    @if(auth()->user())
        <div class="row">
            <form class="col-md-2" action="{{ route('delete_points') }}"
                  method="POST">
                @csrf
                @method('delete')
                <button type="submit" class="btn btn-danger btn-sm" title="Remove Points"
                        onclick="return confirm('Are you sure you want to delete all points');">
                    Delete points
                </button>
            </form>
        </div>
    @endif
    <map-page>
    </map-page>
</div>
</body>
</html>
