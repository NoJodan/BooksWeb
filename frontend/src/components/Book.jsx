import { TruncatedParagraph } from './TruncatedParagraph'

export const Book = ({ name, description, author, className=""}) => {
    
    return (
        <>
            <div className={className === "" ? "card book" : "card book " + className}>
                <div className='card-title'>
                    <h1>{name}</h1>
                </div>
                <div className="card-body">
                    <TruncatedParagraph className="description" text={description} charLimit={200}/>       
                </div>
                <div className="card-footer d-flex justify-content-left">
                    <p>
                        <strong>Author:</strong> {author}
                    </p>
                </div>
                
            </div>
        </>
    )

}