<script lang="ts" setup>
import { onMounted, reactive, Ref, ref } from 'vue';
import Header from './Header.vue';
import Footer from './Footer.vue';
import ResultsCard from './ResultsCard.vue';
import TeamCard from './TeamCard.vue';

export interface TeamTotals {
  failing: number;
  passing: number;
  pending: number;
}

export interface Team {
  name: string;
  totals: TeamTotals;
}

interface SummaryResponse {
  summary: TeamTotals;
  teams: Team[];
}

let teamsResponse = reactive({
  summary: {
    failing: 0,
    passing: 0,
    pending: 0
  },
  teams: []
});

let teams: Team[] = reactive([]);
let totalResults: TeamTotals = reactive({
  failing: 1,
  passing: 2,
  pending: 1
});

async function fetchSummary() {
  const resp = await fetch('http://127.0.0.1:5000/teams/summary')
  const ddd = await resp.json()
  teamsResponse = ddd
  teams = teamsResponse.teams;
  totalResults = teamsResponse.summary;
}

onMounted(async () => {
  await fetchSummary();


  console.log('teamsResponse:', teamsResponse.summary);
  console.log('Teams:', teams);
  console.log('Total Results:', totalResults);
});

</script>

<template>

  <Header/>
  <ResultsCard v-model:totals="totalResults" />
  <div class="w-full max-w-screen-lg my-4 h-1 bg-primary mx-auto"></div>
  <div class="w-full px-4 pb-10">
    <div class="max-w-screen-lg mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <TeamCard
            v-for="team in teams"
            :key="team.name"
            :team="team"
        />
      </div>
    </div>
  </div>
  <Footer/>

</template>

