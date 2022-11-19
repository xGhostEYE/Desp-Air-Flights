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
        <span v-for="item in resultObject.flights">
          <div class="card-body">
            <h5 class="card-title">12:03-14:02</h5>

            <p class="card-text">{{ item.departure.time }} - {{ item.departure.location }} ({{ item.departure['airport code'] }})</p>

            <p class="card-text">{{ item.arrival.time }} - {{ item.arrival.location }} ({{ item.arrival['airport code'] }})</p>
            <p class="card-text">{{ item.airline }}</p>
            <a href="#" class="btn btn-primary" style="background-color: #3E6D9C">Take me to this flight!</a>
            <hr/>
          </div>
        </span>
      </div>
    </li>
  </div>  
</template>

<script>
export default {
  name: "Results",
  /* data() {
    return {
      
    };
  } */
};
</script>