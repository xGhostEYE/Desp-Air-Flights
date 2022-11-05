<template>
  <div class="column">
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
            <button class="mt-5 btn btn-info">Search</button>
          </div>
      </div> 
    </div>

    <div id="flights">
      <button @click="showFlights()">ShowFlights</button>
      <p
          v-if="myFlight">here betsch
    </p>
    </div>
  </div>
 
</template>



<script>
import HomePage from './components/HomePage.vue';
import Flights from './components/FlightPage.vue';

export default {
  name: "App",
  components: {
    Flights,
    HomePage
  },
  data() {
    return {
      airports: null,
      myFlight: false,
      title: "Desp-Air Flights"
    };
  },
  mounted () {
    axios
      .get('cmpt370-api:5000/airports')
      .then(response => (this.airports = response));
  },
  methods: {
    showFlights () {
      this.myFlight = true;
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
