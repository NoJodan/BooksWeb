import { TruncatedParagraph } from './TruncatedParagraph'

export const Book = ({previousId,id, name, description, author, className=""}) => {
    
    return (
        <>
            <div className={className === "" ? "card book" : "card book " + className} id={id}>
                <div className='card-title'>
                    <h1>{name}</h1>
                </div>
                <div className="card-body">
                    <TruncatedParagraph previousId={previousId} id={id} className="description" text={description} charLimit={200}/>       
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