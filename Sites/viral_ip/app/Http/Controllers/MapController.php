<?php

namespace App\Http\Controllers;

use App\Models\Point;
use Log;

class MapController extends Controller
{
    public function lookUp() {
        if ($_SERVER['REMOTE_ADDR'] === '127.0.0.1') {

            $ip = mt_rand(0, 255) . "." . mt_rand(0, 255) . "." . mt_rand(0, 255) . "." . mt_rand(0, 255);
        } else {
            $ip = $_SERVER['REMOTE_ADDR'];
        }

        try {
            $url = "http://api.ipstack.com/{$ip}?access_key=" . env('IP_KEY');
            $json  = json_decode(file_get_contents($url), true);
        } catch (\exception $e) {
            $json = [
                'city' => $this->getRandomCity(),
                'latitude' => rand(0,90),
                'longitude' => rand(0,90),
            ];
        }

        return $json;
    }

    public function getRandomCity() {
        return rand() * 20 .'sville';
    }

    /**
     * Looks up ip
     */
    public function hit() {
        $json = $this->lookUp();

        return Point::firstOrCreate([
            'city' => isset($json['city']) ?: $this->getRandomCity(),
            'latitude' => isset($json['latitude']) ?: rand(0,90),
            'longitude' => isset($json['longitude']) ?: rand(0,90),
        ]);
    }

    /**
     * Grabs points from db
     */
    public function points() {
        $rest = Point::all();
        $mine = $this->hit();

        return [
            'mine' => $mine,
            'rest' => $rest
        ];
    }

    /**
     * Returns map
     */
    public function index() {

        return view('map');
    }

    /**
     * Deletes points
     */
    public function delete() {
        Point::truncate();

        return redirect('/');
    }
}
