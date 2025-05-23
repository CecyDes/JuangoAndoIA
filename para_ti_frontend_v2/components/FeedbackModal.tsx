
import { useState } from "react";
import { X } from "lucide-react";

type Props = {
  recommendation: { title: string };
  onClose: () => void;
};

export default function FeedbackModal({ recommendation, onClose }: Props) {
  const [feedback, setFeedback] = useState("");

  const handleSubmit = () => {
    console.log("Feedback enviado:", feedback);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-2xl w-full max-w-md shadow-lg relative">
        <button onClick={onClose} className="absolute top-2 right-2">
          <X className="w-5 h-5" />
        </button>
        <h2 className="text-xl font-bold mb-2">¿Te gustó "{recommendation.title}"?</h2>
        <textarea
          className="w-full border rounded-xl p-2 mt-2"
          rows={4}
          placeholder="Cuéntanos tu opinión..."
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
        />
        <button
          onClick={handleSubmit}
          className="mt-4 bg-green-500 text-white px-4 py-2 rounded-xl hover:bg-green-600"
        >
          Enviar
        </button>
      </div>
    </div>
  );
}
