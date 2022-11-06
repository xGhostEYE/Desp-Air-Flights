<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
});
</script>

<template>
    <div class="column container d-flex align-items-center justify-content-center">
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
            <button @click="search()" class="mt-5 btn btn-info">Search</button>
          </div>
      </div> 
    </div>
</template>
<script>
export default {
    data() {
      return {
        starting: '',
        destination: '',
        flight_path: {
          starting: '',
          destination: '',
        },
      }
    },
    methods: {
      search(){
        this.$emit('getFlights');
      }
    },
  };
</script>
