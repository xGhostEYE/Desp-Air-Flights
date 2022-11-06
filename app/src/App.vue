<template>
  <div class="col-lg-8">
    <div>
      <div class="title display-1 fixed-top">
        <h1 class="text-center">{{title}}</h1>
      </div>
      <div class="search_box">
        <p class="mb-0">Starting</p>
        <input
          :value="starting"
          @input="event => starting = event.target.value">
          <p class = "mt-5 mb-0">Destination</p>
        <input
          :value="destination"
          @input="event => destination = event.target.value">
          <div>
            <button class="mt-5 btn btn-info" @click="showFlights()">Search</button>
          </div>
      </div> 
    </div>

    <ul class="">
      <li class="list-group-item"><div class="card">1:09pm-3:01pm</div></li>
      <li class="list-group-item"><div class="card">1h 58min</div></li>
      <li class="list-group-item"><div class="card">1</div></li>
    </ul>

    <div id="flights" v-if="myFlight">
      <div class="row">
        <div class="row">
          <div class="time column">
              1:09pm-3:01pm
          </div>
          <div class="travel time column">
              1h 58min
          </div>
          <div class="number of stops column">
              1
          </div>
          <div class="price column">
              $170
          </div>
        </div>
        <div class="row">
          <div class="column">
            hi
          </div>
        </div>
      </div>
    </div>
  </div> 
 
</template>



<script>
import HomePage from './components/HomePage.vue';
import Flights from './components/FlightPage.vue';
import axios from 'axios';

export default {
  name: "App",
  components: {
    Flights,
    HomePage
  },
  data() {
    return {
      airports: null,
      flights: null,
      myFlight: false,
      title: "Desp-Air Flights"
    };
  },
  mounted () {
    axios
      .get('http://127.0.0.1:5000/airports')
      .then(response => (this.airports = response.data));
  },
  methods: {
    async showFlights () {
      this.myFlight = true;
      
      await axios
      .get('http://127.0.0.1:5000/flights')
      .then(response => (this.flights = response.data));

    },
  }
};
</script>



<style>
.p{
  margin-top: 0px;
}
.title{
  background-color: #5F9DF7;
}
</style>
