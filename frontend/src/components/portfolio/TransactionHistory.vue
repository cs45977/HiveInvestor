<script setup>

const props = defineProps({
  transactions: {
    type: Array,
    default: () => []
  }
})

const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleString()
}

const formatCurrency = (value) => {
   return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}
</script>

<template>
  <div class="overflow-x-auto mt-4 bg-white shadow rounded-lg">
    <h3 class="p-4 text-lg font-bold border-b">Transaction History</h3>
    <table class="min-w-full leading-normal">
      <thead>
        <tr>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Date
          </th>
           <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Type
          </th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Symbol
          </th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Qty
          </th>
           <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Price
          </th>
           <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
            Total
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="transactions.length === 0">
            <td colspan="6" class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-center">
                No transactions
            </td>
        </tr>
        <tr v-for="tx in transactions" :key="tx.id">
          <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
            {{ formatDate(tx.timestamp) }}
          </td>
          <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm font-bold" :class="{'text-green-600': tx.type === 'BUY', 'text-red-600': tx.type === 'SELL'}">
            {{ tx.type }}
          </td>
          <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
            {{ tx.symbol }}
          </td>
          <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
            {{ tx.quantity }}
          </td>
           <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
            {{ formatCurrency(tx.price_per_share) }}
          </td>
           <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
            {{ formatCurrency(tx.total_amount) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
