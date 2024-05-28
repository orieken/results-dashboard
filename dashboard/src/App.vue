<script lang="ts">
import { defineComponent, ref } from 'vue';
import Header from './Header.vue';
import Footer from './Footer.vue';
import ResultsCard from './ResultsCard.vue';
import TeamCard from './TeamCard.vue';

export const teamsResponse = {
  teams: [
    {
      name: 'Team 1',
      testResults: {
        passed: 18,
        failed: 2,
        pending: 0
      }
    },
    {
      name: 'Team Alpha',
      testResults: {
        passed: 10,
        failed: 2,
        pending: 2
      }
    },
    {
      name: 'Team B',
      testResults: {
        passed: 1,
        failed: 2,
        pending: 1
      }
    },
    {
      name: 'Team 4 behave',
      testResults: {
        passed: 2,
        failed: 2,
        undefined: 2
      }
    }
  ]
};

export class TestResult {
  passed: number;
  failed: number;
  pending: number;

  constructor(response: { passed: number, failed: number, pending?: number, 'undefined'?: number }) {
    this.passed = response.passed;
    this.failed = response.failed;
    this.pending = response.pending || response.undefined || 0;
  }
}

export class Team {
  name: string;
  testResults: {
    passed: number;
    failed: number;
    pending: number;
  };

  constructor(name: string, testResults: { passed: number, failed: number, pending?: number, 'undefined'?: number }) {
    this.name = name;
    this.testResults = new TestResult(testResults);
  }
}

export class TotalResults {
  passed: number;
  failed: number;
  pending: number;

  constructor(teams: Team[]) {
    this.passed = teams.reduce((acc, team) => acc + team.testResults.passed, 0);
    this.failed = teams.reduce((acc, team) => acc + team.testResults.failed, 0);
    this.pending = teams.reduce((acc, team) => acc + team.testResults.pending, 0);
  }
}

const teams = ref(teamsResponse.teams.map((team: {
  name: string,
  testResults: { passed: number, failed: number, pending?: number, 'undefined'?: number }
}) => new Team(team.name, team.testResults)));
const totalResults = ref(new TotalResults(teams.value));

export default defineComponent({
  components: {
    TeamCard,
    ResultsCard,
    Header,
    Footer,
  },
  setup() {
    return {
      teams,
      totalResults
    };
  }
});
</script>

<template>
  <Header/>
  <ResultsCard :totals="totalResults"/>
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

