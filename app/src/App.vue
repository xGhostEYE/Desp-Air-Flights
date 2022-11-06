<template>
  
    <div>
      <div class="title display-1 fixed-top">
        <h1 class="text-center">{{title}}</h1>
      </div>
    </div>
    <div class="column container d-flex align-items-center justify-content-center">
      <SearchComponent @getFlights="getFlights" airports="" class="column container d-flex align-items-center justify-content-center" />

      <ResultsComponent v-if="showFlights" :results="results" />
    </div> 
 
</template>



<script>
import SearchComponent from './components/SearchComponent.vue';
import ResultsComponent from './components/ResultsComponent.vue';
import axios from 'axios';

export default {
  name: "App",
  components: {
    ResultsComponent,
    SearchComponent
  },
  data() {
    return {
      airports: null,
      results: null,
      showFlights: false,
      title: "Desp-Air Flights"
    };
  },
  mounted () {
    axios
      .get('http://127.0.0.1:5000/airports')
      .then(response => (this.airports = response.data));
  },
  methods: {
    async getFlights () {
      this.showFlights = true;
      console.log("its working");
      
      await axios
      .get('http://127.0.0.1:5000/flights')
      .then(response => (this.results = response.data));

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
