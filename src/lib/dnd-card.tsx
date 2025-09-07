
export type Ability = {
  name: string,
  abbrev: string,
  modifier: number,
  isElement: boolean,
  score: number
};

export function DNDCardList(props: { children?: React.ReactNode }) {
  return (
    <div className="table-view">
      {props.children}
    </div>
  )
}

export default function DNDCard(props: Ability) {
  const modifierPrefix = props.modifier >= 0 ? '+' : '';
  const className = `dnd-card ${props.isElement ? 'element' : ''}`;

  return (
    <div className={className}>
      <h3>{props.abbrev}</h3>
      <div className="score">{props.score}</div>
      <span>({`${modifierPrefix}${props.modifier}`})</span>
      <div>{props.name}</div>
    </div>
  )
}