const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const readline = require('readline');

const packageDefinition = protoLoader.loadSync("sintomas.proto", {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});
const sintomasProto = grpc.loadPackageDefinition(packageDefinition).sintomas;

const client = new sintomasProto.SintomasService(
  'localhost:50051',
  grpc.credentials.createInsecure()
);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Digite os sintomas separados por vírgula: ', (resposta) => {
  const sintomas = resposta.split(',').map(s => s.trim());

  client.Analisar({ sintomas }, (err, res) => {
    if (err) {
      console.error('Erro:', err);
    } else {
      console.log('✅ Diagnóstico:', res.diagnostico);
      console.log('🩺 Recomendação:', res.recomendacao);
    }
    rl.close();
  });
});
