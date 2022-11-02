<script>
import Flights from './components/FlightPage.vue';
import HomePage from './components/HomePage.vue';
export default {
  name: "App",
  components: {
    Flights,
    HomePage
  },
  data() {
    return {
      title: "Desp-Air Flights",
      myFlight: false
    };
  },
  methods: {
    showFlights () {
      this.myFlight = true;
    },
  }
};
</script>

<template>
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
  <!-- <div id="flights">
    <button @click="showFlights">Search</button>
    <first-component
        v-if="myFlight"
    />
  </div> -->
 
</template>







<style>
.p{
  margin-top: 0px;
}
.title{
  background-color: #5F9DF7;
}
</style>
