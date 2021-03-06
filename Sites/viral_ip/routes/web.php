<?php

use App\Http\Controllers\MapController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Auth::routes();

Route::get('/', [MapController::class, 'index'])->name('index');

Route::get('/points', [MapController::class, 'points'])->name('points');

Route::delete('/points/delete', [MapController::class, 'delete'])->name('delete_points');
