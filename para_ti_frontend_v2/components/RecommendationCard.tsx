
type Props = {
  data: { id: number; title: string; description: string };
  onFeedback: () => void;
};

export default function RecommendationCard({ data, onFeedback }: Props) {
  return (
    <div className="rounded-2xl shadow-lg p-4 bg-white hover:shadow-xl transition">
      <h2 className="text-xl font-semibold">{data.title}</h2>
      <p className="text-gray-600 mt-2">{data.description}</p>
      <button
        onClick={onFeedback}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-xl hover:bg-blue-600"
      >
        ¿Te gustó esta recomendación?
      </button>
    </div>
  );
}
