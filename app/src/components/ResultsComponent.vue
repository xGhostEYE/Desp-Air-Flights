<script setup>
defineProps({
  results: {
    type: Object,
    required: true
  }
});
</script>


<template>
  <div class="column" style="height:1px; width: 1000px;">
    <li v-for="resultObject in this.results">
      <div class="card w-75">
        <div class="card-body">
          <h5 class="card-header">{{ resultObject.startTime }} - {{ resultObject.endTime }}    {{ resultObject.totalTime }}    {{ resultObject.totalCost }}</h5>
          <span v-for="item in resultObject.flights">
            <p class="card-text">{{ item.departure.time }}   -    {{ item.departure.location }} ({{ item.departure['airport code'] }})</p>
            
            <img src="node_modules/bootstrap-icons/icons/stop.svg" alt="">
            <div class="vr"></div>
            <img src="node_modules/bootstrap-icons/icons/stop.svg" alt="">

            <p class="card-text">{{ item.arrival.time }}   -    {{ item.arrival.location }} ({{ item.arrival['airport code'] }})</p>

            <p class="card-text">{{ item.airline }}</p>
            <button @click="redirectToFlight(resultObject.url)" class="mt-5 btn btn-primary" style="background-color: #3E6D9C;">Take me to this flight!</button>

            <hr/>
          </span>
        </div>  
      </div>
    </li>
  </div>  
</template>




<script>
export default {
  name: "Results",
  methods: {
      redirectToFlight: function(url){
        window.open(url)
      }
  /* data() {
    return {
      
    };
  } */
  }
};
</script>