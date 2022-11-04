<template>
  <div class="column">
    <div>
      <div class="title display-1 fixed-top">
        <h1 class="text-center">{{title}}</h1>
      </div>
    </div>
    <HomePage></HomePage>

    <div id="flights">
      <button @click="showFlights">Search</button>
      <first-component
          v-if="showComponentOne"
      />
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
      myFlight: false,
      title: "Desp-Air Flights"
    };
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
