
<script setup>
import { formatarCentavos } from '../format'
import { LIMITE_ESTOQUE_BAIXO } from '../constants'

defineProps({
  produtos: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['movimentar'])
</script>

<template>
  <div class="tabela-container">
    <table>
      <thead>
        <tr>
          <th>SKU</th>
          <th>Nome</th>
          <th>Estoque</th>
          <th>Custo médio</th>
          <th>Margem</th>
          <th>Preço de venda</th>
          <th>Ações</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="produto in produtos" :key="produto.id">
          <td>{{ produto.sku }}</td>
          <td>{{ produto.nome }}</td>

          <td
            :class="{
              baixo: produto.estoque <= LIMITE_ESTOQUE_BAIXO
            }"
          >
            {{ produto.estoque }}
          </td>

          <td>
            {{ formatarCentavos(produto.custo_medio_centavos) }}
          </td>

          <td>{{ produto.margem_percentual }}%</td>

          <td>
            {{ formatarCentavos(produto.preco_venda_centavos) }}
          </td>

          <td class="acoes">
            <button
              @click="emit('movimentar', {
                produto,
                tipo: 'compra'
              })"
            >
              Compra
            </button>

            <button
              class="secundario"
              :disabled="produto.estoque === 0"
              @click="emit('movimentar', {
                produto,
                tipo: 'saida'
              })"
            >
              Saída
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
