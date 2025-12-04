<script setup>

const props = defineProps({
  holdings: {
    type: Array,
    default: () => []
  }
})

const formatCurrency = (value) => {
   return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}
</script>

<template>
  <div class="overflow-x-auto mt-4 bg-white shadow rounded-lg">
    <table class="min-w-full leading-normal">
      <thead>
        <tr>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Symbol
          </th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Quantity
          </th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Avg. Cost
          </th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Last Price
          </th>
           <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Market Value
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="holdings.length === 0">
            <td colspan="5" class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-center">
                No holdings
            </td>
        </tr>
        <tr v-for="holding in holdings" :key="holding.symbol">
          <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm font-bold">
            {{ holding.symbol }}
          </td>
          <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
            {{ holding.quantity }}
          </td>
           <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right text-gray-500">
            {{ formatCurrency(holding.average_price) }}
          </td>
          <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
            {{ formatCurrency(holding.current_price || holding.average_price) }}
          </td>
           <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right font-bold">
            {{ formatCurrency(holding.quantity * (holding.current_price || holding.average_price)) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
