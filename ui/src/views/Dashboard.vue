<template>
  <div>
    <h1>{{$t('dashboard.title')}}</h1>
    <!-- error message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
      <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
        <span class="pficon pficon-close"></span>
      </button>
      <span class="pficon pficon-error-circle-o"></span>
      {{ errorMessage }}.
    </div>

    <div v-show="!uiLoaded" class="spinner spinner-lg"></div>
    <div v-show="uiLoaded">

      <!-- rspamd -->
      <div class="row" v-if="uiLoaded">
        <h3>{{ $t('dashboard.email_protection') }}</h3>
        <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
          <span class="card-pf-utilization-card-details-count stats-count">
            <span
              :class="dashboardData.rspamd.active ? 'fa fa-check green' : 'fa fa-times red'"
            ></span>
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.status') }}
            </span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ dashboardData.rspamd.malwareFound }}
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.malware_found') }}
            </span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ dashboardData.rspamd.signatures }}
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.signatures_loaded') }}
            </span>
          </span>
        </div>
      </div>

      <!-- rspamd malware chart -->
      <div class="row">
        <div
          id="pie-chart-rspamd"
          v-show="uiLoaded && dashboardData.rspamd.malwareStats.length > 0"
        ></div>
        <div v-show="uiLoaded && dashboardData.rspamd.malwareStats.length == 0" class="empty-piechart">
          <div class="fa fa-pie-chart"></div>
          <div>{{$t('dashboard.no_data_available')}}</div>
        </div>
      </div>

      <div class="divider"></div>

      <!-- squidclamav -->
      <div class="row" v-if="uiLoaded">
        <h3>{{ $t('dashboard.web_protection') }}</h3>

        <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
          <span class="card-pf-utilization-card-details-count stats-count">
            <span
              :class="dashboardData.squidclamav.active ? 'fa fa-check green' : 'fa fa-times red'"
            ></span>
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.status') }}
            </span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
          <span
            class="card-pf-utilization-card-details-count stats-count"
          >{{ dashboardData.squidclamav.malwareFound }}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.malware_found') }}</span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ dashboardData.squidclamav.signatures }}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.signatures_loaded') }}</span>
          </span>
        </div>
      </div>
      
      <!-- squidclamav malware chart -->
      <div class="row">
        <div
          id="pie-chart-squidclamav"
          v-show="uiLoaded && dashboardData.squidclamav.malwareStats.length > 0"
        ></div>
        <div v-show="uiLoaded && dashboardData.squidclamav.malwareStats.length == 0" class="empty-piechart">
          <div class="fa fa-pie-chart"></div>
          <div>{{$t('dashboard.no_data_available')}}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  props: {
  },
  mounted() {
    this.getDashboardData()
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      dashboardData: {
        "rspamd": null,
        "squidclamav": null
      },
    };
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error) /* eslint-disable-line no-console */
      this.errorMessage = errorMessage
    },
    closeErrorMessage() {
      this.errorMessage = null
    },
    getDashboardData() {
      var ctx = this;
      nethserver.exec(
        ["nethserver-antivirus/dashboard/read"],
        null,
        null,
        function(success) {
          success = JSON.parse(success);
          ctx.dashboardData = success;
          ctx.uiLoaded = true;

          setTimeout(function() {
            ctx.initEmailMalwareChart();
            ctx.initWebMalwareChart();
          }, 250);
        },
        function(error) {
          ctx.showErrorMessage(ctx.$i18n.t("dashboard.error_getting_dashboard_data"), error)
        }
      );
    },
    initEmailMalwareChart() {
      var c3ChartDefaults = $().c3ChartDefaults();

      var pieData = {
        type : 'pie',
        columns: this.groupSmallPieCategories(this.dashboardData.rspamd.malwareStats)
      };

      var pieChartConfig = c3ChartDefaults.getDefaultPieConfig();
      pieChartConfig.bindto = '#pie-chart-rspamd';
      pieChartConfig.data = pieData;
      pieChartConfig.legend = {
        show: true,
        position: 'right'
      };
      pieChartConfig.size = {
        width: 481,
        height: 251
      };
      pieChartConfig.color={ pattern:[
        $.pfPaletteColors.orange,
        $.pfPaletteColors.red,
        $.pfPaletteColors.blue,
        $.pfPaletteColors.green,
        $.pfPaletteColors.gold,
        $.pfPaletteColors.purple,
        $.pfPaletteColors.black
      ]};
      var pieChartLegend = c3.generate(pieChartConfig);
    },
    initWebMalwareChart() {
      var c3ChartDefaults = $().c3ChartDefaults();

      var pieData = {
        type : 'pie',
        columns: this.groupSmallPieCategories(this.dashboardData.squidclamav.malwareStats)
      };

      var pieChartConfig = c3ChartDefaults.getDefaultPieConfig();
      pieChartConfig.bindto = '#pie-chart-squidclamav';
      pieChartConfig.data = pieData;
      pieChartConfig.legend = {
        show: true,
        position: 'right'
      };
      pieChartConfig.size = {
        width: 481,
        height: 251
      };
      pieChartConfig.color={ pattern:[
        $.pfPaletteColors.orange,
        $.pfPaletteColors.red,
        $.pfPaletteColors.blue,
        $.pfPaletteColors.green,
        $.pfPaletteColors.gold,
        $.pfPaletteColors.purple,
        $.pfPaletteColors.black
      ]};
      var pieChartLegend = c3.generate(pieChartConfig);
    },
    groupSmallPieCategories(pieData) {
      var threshold = 5
      var groupedLabel = this.$i18n.t("dashboard.other")
      var groupedValue = 0
      var i = pieData.length

      while (i--) {
        if (pieData[i][1] < threshold) {
            groupedValue += pieData[i][1]
            pieData.splice(i, 1);
        }
      }

      if (groupedValue > 0) {
        // some categories have been grouped together
        pieData.push([ groupedLabel, groupedValue])
      }
      return pieData
    }
  }
};
</script>

<style>
.row {
  padding-left: 20px;
  padding-right: 20px;
}

.empty-piechart {
  margin-top: 2em;
  margin-bottom: 2em;
  text-align: center;
  color: #9c9c9c;
}
.empty-piechart .fa {
  font-size: 200px;
  color: #bbbbbb;
}
</style>
