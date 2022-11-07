<template>
  <p hidden>Hello Vitest</p>
    <TitleComponent />
    <div class="column container d-flex align-items-center justify-content-center">
      <SearchComponent @getFlights="getFlights" airports="" class="" />
      <br>
      <ResultsComponent v-if="showFlights" :results="results" />
    </div> 
 
</template>



<script>
import SearchComponent from './components/SearchComponent.vue';
import ResultsComponent from './components/ResultsComponent.vue';
import axios from 'axios';
import TitleComponent from './components/TitleComponent.vue';

export default {
  name: "App",
  components: {
    ResultsComponent,
    SearchComponent,
    TitleComponent
},
  data() {
    return {
      airports: null,
      results: null,
      showFlights: false,
      baseURL: "http://127.0.0.1:5000"
    };
  },
  mounted () {
    axios
      .get(this.baseURL + '/airports')
      .then(response => (this.airports = response.data));
  },
  methods: {
    async getFlights (dep, des) {
      this.showFlights = true;
      
      await axios
        .get(this.baseURL + '/flights', {
          params: {
            departure: String(dep),
            destination: String(des)
          }
        })
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
