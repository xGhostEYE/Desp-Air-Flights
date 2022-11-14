<script setup>
defineProps({
  results: {
    type: Object,
    required: true
  }
});
</script>

<template>
  {{this.results}}
  <div class="container d-flex align-items-center justify-content-center">
    <ul>
      <li class="list-group-item">
        <div class="card">
          {{ this.flights }}
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
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Results",
  data() {
    return {
      
    };
  }
};
</script>