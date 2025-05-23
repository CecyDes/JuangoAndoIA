
import { useState } from "react";
import RecommendationCard from "@/components/RecommendationCard";
import FeedbackModal from "@/components/FeedbackModal";
import { User, ShoppingCart, Globe, Settings } from "lucide-react";

const mockRecommendations = [
  { id: 1, title: "Balón de fútbol", description: "Balón profesional para tus partidos" },
  { id: 2, title: "Raqueta de tenis", description: "Raqueta ligera para un mejor rendimiento" },
  { id: 3, title: "Bicicleta de montaña", description: "Para las rutas más exigentes" },
  { id: 4, title: "Pesas ajustables", description: "Entrena en casa con diferentes niveles" },
  { id: 5, title: "Zapatos deportivos", description: "Comodidad y estilo para correr" },
  { id: 6, title: "Camiseta transpirable", description: "Mantente fresco durante el ejercicio" },
];

export default function Home() {
  const [selectedRec, setSelectedRec] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleFeedbackClick = (rec) => {
    setSelectedRec(rec);
    setShowModal(true);
  };

  return (
    <div className="p-4">
      {/* Top Bar */}
      <div className="flex items-center justify-between mb-6">
        <div className="w-3/10 text-2xl font-bold">JUGANDO ANDO</div>
        <div className="w-3/10">
          <input
            type="text"
            placeholder="Buscar productos..."
            className="w-full p-2 border rounded-xl"
          />
        </div>
        <div className="w-4/10 flex justify-around">
          <User className="w-6 h-6" />
          <ShoppingCart className="w-6 h-6" />
          <Globe className="w-6 h-6" />
          <Settings className="w-6 h-6" />
        </div>
      </div>

      {/* Recommendations Grid */}
      <h1 className="text-2xl font-bold mb-4">Para ti</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {mockRecommendations.map((rec) => (
          <RecommendationCard key={rec.id} data={rec} onFeedback={() => handleFeedbackClick(rec)} />
        ))}
      </div>

      {showModal && selectedRec && (
        <FeedbackModal
          recommendation={selectedRec}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  );
}
