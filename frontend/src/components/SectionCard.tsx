interface SectionCardProps {
  name: string;
  questions: number;
}

export default function SectionCard({
  name,
  questions,
}: SectionCardProps) {
  return (
    <div>
      <h3>{name}</h3>

      <p>
        Questions: {questions}
      </p>
    </div>
  );
}