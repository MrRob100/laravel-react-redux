<?php

namespace App\Http\Controllers;

use App\Models\Point;
use Illuminate\Support\Facades\Log;

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
            Log::error($e->getMessage());
            $json = [];
        }

        return $json;
    }

    /**
     * Looks up ip
     */
    public function hit() {
        $json = $this->lookUp();

        $pointFake = Point::factory()->create();

        return Point::firstOrCreate([
            'city' => isset($json['city']) ?: $pointFake->city,
            'latitude' => isset($json['latitude']) ?: $pointFake->latitude,
            'longitude' => isset($json['longitude']) ?: $pointFake->longitude,
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
