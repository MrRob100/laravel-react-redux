<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class PointFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'city' => $this->faker->city(),
            'latitude' => $this->faker->numberBetween(-80, 80),
            'longitude' => $this->faker->numberBetween(-80, 80),
        ];
    }
}
